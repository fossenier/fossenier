
type SSym = String;

type SResult = Result<SVal, String>;
    
#[derive (Clone)]

// SVal ::= String
//       |  Number
//       |  Bool
// ,..
enum SVal {
    VStr  ( String ),            // SVal::VStr
    VNum  ( i32    ),
    VBool ( bool   ),

    VNull,			// dotted pairs
    VPair ( Box<SVal>,
	    Box<SVal> ),
	
    VFun  ( Vec<SSym>,
	    SExp,
	    SEnv ),
    
    VPrim ( SSym )
}

use SVal::*;

#[derive(Clone)]
enum SExp {
    // literals
    EStr    ( String ),		// "abc"
    ENum    ( i32    ),		//  123
    EBool   ( bool   ),		// #t   #f

    // conditional
    EIf     ( Box<SExp>,	// (if .Test.
	      Box<SExp>,	//     .Consequent.
	      Box<SExp> ),	//     .Alternate.   )


    // variables and bindings
    EVar    ( SSym ),			//  .Id.
    ELet    ( Vec<(SSym, SExp)>,	// (let ([.Id. .Exp.] ... )
	      Box<SExp> ),		//       .Body. )
    ERec    ( Vec<(SSym,		// (letrec ([.Id. (lambda (.Id. ...) .Exp.)]
		   (Vec<SSym>, SExp))>,	//          ... )
	      Box<SExp> ),		//          .Body. )

    // sequencing
    ESeq    ( Vec<SExp>	),	// (begin .SExp. ... )
    ENull,                      // ()   -- (begin ) is INVALID syntax
		   
    // functions
    ELam    ( Vec<SSym>,	// (lambda (.Id. ...)
	      Box<SExp> ),	//     .Exp. )
    EApp    ( Box<SExp>,	// ( .Exp.
	      Vec<SExp> )	//         ... )

}

use SExp::*;

#[derive(Clone)]
enum SEnv {
    REmpty,
    RScope ( Vec<(SSym, SVal)>,
	     Box<SEnv> ),
    RRec ( Vec<(SSym,
		(Vec<SSym>, SExp))>,
	   Box<SEnv> )
}

use SEnv::*;

// lookup
fn lookup(s : SSym, r : SEnv) -> SResult {
    match r {
	REmpty             => Err("variable not found".to_string()),
	RScope(bs, _r)     =>
	    match find(s.clone(), bs) {
		Some(v) => Ok(v),
		None    => lookup(s, *_r)
	    },
		    
	RRec(ref yysess, ref _r) =>
	    match findr(s.clone(), yysess) {
		Some((ys, e)) => Ok(VFun(ys, e, r)),
		None          => lookup(s, (**_r).clone())
	    }
    }
}
    
fn find(s : SSym, bs : Vec<(SSym, SVal)>) -> Option<SVal> {
    match bs.iter().find(|(y,_)| *y == s) {
	Some((_, v)) => Some(v.clone()),
	None => None
    }
}

fn findr(s : SSym, yysess : &Vec<(SSym, (Vec<SSym>, SExp))>)
	 -> Option<(Vec<SSym>, SExp)> {
    match yysess.iter().find(|(y,_)| *y == s) {
	Some((_, (ys, e))) => Some((ys.clone(), e.clone())),
	None               => None
    }
}

fn display(v : SVal) -> () {
    match v {
	VStr(s)      => print!("{}", s),
	VNum(z)      => print!("{}", z),
	VBool(b)     => print!("{}", if b { "#t" } else { "#f" }),
	VFun(_,_,_)  => print!("{}", "function"),
	VPrim(_)     => print!("{}", "primitive"),
	VNull        => print!("{}", "null"),
	VPair(_,_)   => print!("{}", "pair")
    }
}

// primitives
fn prim(y : SSym, vs : Vec<SVal>) -> SResult {
    match y.as_str() {
	"cons" => match vs.get(0) {
	    Some(v1) => match vs.get(1) {
		Some(v2) => Ok(VPair(Box::new(v1.clone()),
				     Box::new(v2.clone()))),
		None => Err("cons is binary".to_string())
	    },
	    None => Err("cons is binary".to_string())
	},

	"car" => match vs.get(0) {
	    Some(VNull)        => Err("empty list".to_string()),
	    Some(VPair(_v, _)) => Ok(*_v.clone()),
	    _                  => Err("not a list".to_string())
        },

	"cdr" => match vs.get(0) {
	    Some(VNull)        => Err("empty list".to_string()),
	    Some(VPair(_, _l)) => Ok(*_l.clone()),
	    _                  => Err("not a list".to_string())
	},

	"null?" => match vs.get(0) {
	    Some(VNull)      => Ok(VBool(true)),
	    Some(VPair(_,_)) => Ok(VBool(false)),
	    _                => Err("not a list".to_string())
	},
	
	"display!" => match vs.get(0) {
	    Some(v) => { display(v.clone());
			 Ok(VNull) },
	    None    => Err("nothing to display".to_string())
	},

	_ => match vs.get(0) {
	    Some(VNum(n)) => match vs.get(1) {
		Some(VNum(m)) => match y.as_str() {
		    "+"  => Ok(VNum(n + m)),
		    "-"  => Ok(VNum(n - m)),
		    "*"  => Ok(VNum(n * m)),
		    "<"  => Ok(VBool(n <  m)),
		    "<=" => Ok(VBool(n <= m)),
		    "="  => Ok(VBool(n == m)),
		    ">=" => Ok(VBool(n >= m)),
		    ">"  => Ok(VBool(n >  m)),
		    _    => Err("unknown arithmetic".to_string())
                },
		_       => Err("second operand not integer".to_string())
            },
	    
	    Some(VStr(s)) => match vs.get(1) {
		Some(VStr(t)) => match y.as_str() {
		    "+" => Ok(VStr(s.to_owned()+t)),
		    "=" => Ok(VBool(s == t)),
		    _   => Err("unknown string op".to_string())
		},
		_       => Err("first operand not comparable".to_string())
	    },

	    None => Err("unrecognized nonary primitive".to_string()),

	    _ => Err("unknown primitive".to_string())

	}
    }
}


use std::iter::*;

fn eval(e : SExp, r : SEnv) -> SResult {
    match e {
	EStr(s)  => Ok(VStr(s)),
	ENum(z)  => Ok(VNum(z)),
	EBool(b) => Ok(VBool(b)),
    
	EIf(t, c, a) => match eval(*t, r.clone()) {
	    Ok(VBool(true))  => eval(*c, r),
	    Ok(VBool(false)) => eval(*a, r),
	    _                => Err("non-boolean test".to_string())
	},

	EVar(y) => lookup(y, r),
	ELet(yes, b) => { let yus = evals(yes, &r);
			  if yus.iter().fold(true, |b, (_, u)| b && match u { Ok(_)  => true,
									      Err(_) => false }) {
			      eval(*b, RScope(yus.iter().map(|(y, u)| match u { Err(_) => panic!("err found in vector containing no errors"),
										Ok(v)  => (y.clone(), v.clone()) }).collect(), Box::new(r)))
			  } else {
			      Err("invalid argument".to_string())
			  }
	}

	ERec(yysess, b) => eval(*b, RRec(yysess, Box::new(r.clone()))),
	
	ESeq(es) => es.iter().fold(Ok(VNull), |u, e| match u { Err(s) => Err(s),
							       Ok(_)  => eval(e.clone(), r.clone())}),
    	
	ELam(ys, b) => Ok(VFun(ys, *b, r.clone())),
	    
	EApp(e, es) => match eval(*e, r.clone()) {
	    Ok(VFun(ys, b, rl)) => { let yes = ys.iter().zip(es.iter()).map(|(y, e)| (y.clone(), e.clone())).collect();
				     let yus = evals(yes, &r);
				     if yus.iter().fold(true, |b, (_, u)| b && match u { Ok(_)  => true,
											Err(_) => false }) {
					 eval(b, RScope(yus.iter().map(|(y, u)| match u { Err(_) => panic!("err found in vector containing no errors"),
											  Ok(v) => (y.clone(), v.clone()) }).collect(),
							//Box::new(top_r)))       // static scoping
							//Box::new(r)))             // dynamic scoping
							Box::new(rl)))            // lexical scoping
				     } else {
					 Err("invalid argument".to_string())
				     }
	                           },

	    Ok(VPrim(y)) => { let us : Vec<SResult> = es.iter().map(|e| eval(e.clone(), r.clone())).collect();
			      if us.iter().fold(true, |b, u| b && match u { Ok(_) => true,
									    Err(_) => false }) {
				  prim(y, us.iter().map(|u| match u { Err(_) => panic!("error found in vector containing no errors"),
								      Ok(v) => v.clone()}).collect())
			      } else {
				  Err("arguments to prim ".to_string()+&y)
			      }
	                    },

	    Err(s) => Err(("not a function/primitive: ".to_owned()+&s).to_string()),

	    _ => Err("huh".to_string())
	},
	
	ENull => Ok(VNull)
    }
}

fn evals(yes : Vec<(SSym, SExp)>, r : &SEnv) -> Vec<(SSym, SResult)> {
    yes.iter().map(|(y,e)| (y.clone(), eval(e.clone(), r.clone()))).collect()
}

fn print(v : SResult) {
    match v {
	Ok(v) => display(v),
	Err(s) => print!("Err: {}", s)
    }
    println!()
}
	    

fn main() {
    print!("A ");
    // "hello"
    print(eval(EStr("hello".to_string()), REmpty));

    print!("B ");
    // 3
    print(eval(ENum(3), REmpty));

    print!("C ");
    // #t
    print(eval(EBool(true), REmpty));

    print!("D ");
    // (if #t 3 4)
    print(eval(EIf(Box::new(EBool(true)),
		   Box::new(ENum(3)),
		   Box::new(ENum(4))), REmpty));

    print!("E ");
    // (if #f 3 4)
    print(eval(EIf(Box::new(EBool(false)),
		   Box::new(ENum(3)),
		   Box::new(ENum(4))), REmpty));

    print!("F ");
    // (let ([a 1] [b 2]) a)
    //  identical to
    // ((lambda (a b) a) 1 2)
    print(eval(ELet(vec![("a".to_string(), ENum(1)),
			 ("b".to_string(), ENum(2))],
		    Box::new(EVar("a".to_string()))), REmpty));

    // (let ([incr (lambda (n) (+ n 1))])
    //    (incr 2)
    
    print!("G ");
    // (let ([a 1] [b 2]) (let ([a b] [c 3]) a))
    print(eval(ELet(vec![("a".to_string(), ENum(1)),
			 ("b".to_string(), ENum(2))],
		    Box::new(ELet(vec![("a".to_string(), EVar("b".to_string())),
				       ("c".to_string(), ENum(3))],
				  Box::new(EVar("a".to_string()))))), REmpty));


    print!("H ");
    // (let ([a 1] [b 2]) b)
    print(eval(ELet(vec![("a".to_string(), ENum(3)),
			 ("b".to_string(), ENum(4))],
		    Box::new(EVar("b".to_string()))), REmpty));

    // a top-level environment, populated with primitives
    let top_r = RScope(vec![("+".to_string(), VPrim("+".to_string())),
			    ("-".to_string(), VPrim("-".to_string())),
			    ("*".to_string(), VPrim("*".to_string())),
			    ("<".to_string(),  VPrim("<".to_string())),
			    ("<=".to_string(), VPrim("<=".to_string())),
			    ("=".to_string(),  VPrim("=".to_string())),
			    (">=".to_string(), VPrim(">=".to_string())),
			    (">".to_string(),  VPrim(">".to_string())),
			    ("null".to_string(), VNull),
			    ("car".to_string(),  VPrim("car".to_string())),
			    ("cdr".to_string(),  VPrim("cdr".to_string())),
			    ("cons".to_string(), VPrim("cons".to_string())),
			    ("null?".to_string(), VPrim("null?".to_string())),
			    ("display!".to_string(), VPrim("display!".to_string()))],
		       Box::new(REmpty));

    print!("I ");
    // (let ([+ (lambda (x y) (- (+ x y) 1))]) (+ 1 2))
    print(eval(ELet(vec![("+".to_string(), ELam(vec!["x".to_string(), "y".to_string()],
						Box::new(EApp(Box::new(EVar("-".to_string())),
							      vec![EApp(Box::new(EVar("+".to_string())),
									vec![EVar("x".to_string()),
									     EVar("y".to_string())]),
								   ENum(1)]))))],
		    Box::new(EApp(Box::new(EVar("+".to_string())),
				  vec![ENum(1),
				       ENum(2)]))),
	  top_r.clone()));
    
    print!("J ");
    // (let ([a 1] [b 2]) (+ a b))
    print(eval(ELet(vec![("a".to_string(), ENum(3)),
			 ("b".to_string(), ENum(4))],
		    Box::new(EApp(Box::new(EVar("+".to_string())),
				  vec![EVar("a".to_string()),
				       EVar("b".to_string())]))),
	       top_r.clone()));

    print!("K ");
    // (let ([a 1] [b 2]) (if (> a b) (+ a b) (- a b)))
    print(eval(ELet(vec![("a".to_string(), ENum(3)),
			 ("b".to_string(), ENum(4))],
		    Box::new(EIf(Box::new(EApp(Box::new(EVar(">".to_string())),
					       vec![EVar("a".to_string()),
						    EVar("b".to_string())])),
				 Box::new(EApp(Box::new(EVar("+".to_string())),
					       vec![EVar("a".to_string()),
						    EVar("b".to_string())])),
				 Box::new(EApp(Box::new(EVar("-".to_string())),
					       vec![EVar("a".to_string()),
						    EVar("b".to_string())]))))),
	       top_r.clone()));

    print!("L ");
    // (let ([id (lambda (i) i)]) (id 3))
    print(eval(ELet(vec![("id".to_string(), ELam(vec!["i".to_string()],
						 Box::new(EVar("i".to_string()))))],
		    Box::new(EApp(Box::new(EVar("id".to_string())),
				  vec![ENum(3)]))),
	       top_r.clone()));
    
    print!("M ");
    // ((lambda (i) i) 4)
    print(eval(EApp(Box::new(ELam(vec!["i".to_string()],
				  Box::new(EVar("i".to_string())))),
		    vec![ENum(3)]),
	       top_r.clone()));

    print!("N ");
    // (let ([+ (lambda (x y) (- (+ x y) 1))]) (+ 1 2))
    print(eval(ELet(vec![("+".to_string(), ELam(vec!["x".to_string(), "y".to_string()],
						Box::new(EApp(Box::new(EVar("-".to_string())),
							      vec![EApp(Box::new(EVar("+".to_string())),
									vec![EVar("x".to_string()),
									     EVar("y".to_string())]),
								   ENum(1)]))))],
		    Box::new(EApp(Box::new(EVar("+".to_string())),
				  vec![ENum(1),
				       ENum(2)]))),
	  top_r.clone()));

    print!("O ");
    // (let ([i 1])
    //    (let ([f (lambda (x) (+ x i))])
    //       (let ([i 2])
    //          (f 3))))
    print(eval(ELet(vec![("i".to_string(), ENum(1))],
		    Box::new(ELet(vec![("f".to_string(), ELam(vec!["x".to_string()],
							      Box::new(EApp(Box::new(EVar("+".to_string())),
									    vec![EVar("x".to_string()),
										 EVar("i".to_string())]))))],
				  Box::new(ELet(vec![("i".to_string(), ENum(2))],
						Box::new(EApp(Box::new(EVar("f".to_string())),
							      vec![ENum(3)]))))))),
	       top_r.clone()));

    print!("P ");
    // (let ([double (lambda (n) (+ n n))]
    //       [twice  (lambda (f)
    //                  (lambda (n) (f (f n))))])
    //    ((twice double) 2))
    print(eval(ELet(vec![("double".to_string(),
			  ELam(vec!["n".to_string()],
			       Box::new(EApp(Box::new(EVar("+".to_string())),
					     vec![EVar("n".to_string()),
						  EVar("n".to_string())])))),
			 ("twice".to_string(),
			  ELam(vec!["f".to_string()],
			       Box::new(ELam(vec!["n".to_string()],
					     Box::new(EApp(Box::new(EVar("f".to_string())),
							   vec![EApp(Box::new(EVar("f".to_string())),
								     vec![EVar("n".to_string())])]))))))],
		    Box::new(EApp(Box::new(EApp(Box::new(EVar("twice".to_string())),
						vec![EVar("double".to_string())])),
				  vec![ENum(3)]))),
	  top_r.clone()));

    print!("Q ");
    // (let ([double (lambda (n) (+ n n))]
    //       [twice  (lambda (f)
    //                  (lambda (n) (f (f n))))])
    //    (let ([doubletwice (twice double)])
    //       (doubletwice 3)))
    print(eval(ELet(vec![("double".to_string(),
			  ELam(vec!["n".to_string()],
			       Box::new(EApp(Box::new(EVar("+".to_string())),
					     vec![EVar("n".to_string()),
						  EVar("n".to_string())])))),
			 ("twice".to_string(),
			  ELam(vec!["f".to_string()],
			       Box::new(ELam(vec!["n".to_string()],
					     Box::new(EApp(Box::new(EVar("f".to_string())),
							   vec![EApp(Box::new(EVar("f".to_string())),
								     vec![EVar("n".to_string())])]))))))],
		    Box::new(ELet(vec![("doubletwice".to_string(),
					EApp(Box::new(EVar("twice".to_string())),
					     vec![EVar("double".to_string())]))],
				  Box::new(EApp(Box::new(EVar("doubletwice".to_string())),
						vec![ENum(3)]))))),
	       top_r.clone()));

    print!("R ");
    // (letrec ([fact (lambda (n)
    //                   (if (< n 2) 1 (* n (fact (- n 1)))))])
    //    (fact 5))
    print(eval(ERec(vec![("fact".to_string(), (vec!["n".to_string()],
                                               EIf(Box::new(EApp(Box::new(EVar("<".to_string())),
                                                                 vec![EVar("n".to_string()),
                                                                      ENum(2)])),
                                                   Box::new(ENum(1)),
                                                   Box::new(EApp(Box::new(EVar("*".to_string())),
                                                                 vec![EVar("n".to_string()),
                                                                      EApp(Box::new(EVar("fact".to_string())),
                                                                           vec![EApp(Box::new(EVar("-".to_string())),
                                                                                     vec![EVar("n".to_string()),
                                                                                          ENum(1)])])])))))],
                    Box::new(EApp(Box::new(EVar("fact".to_string())),
                                   vec![ENum(5)]))),
               top_r.clone()));


    print!("S ");
    // (letrec ([even? (lambda (n)
    //                    (if (= n 0) #t (odd? (- n 1))))]
    //          [odd?  (lambda (n)
    //                    (if (= n 0) #f (even? (- n 1))))])
    //    (even? 5))
    print(eval(ERec(vec![("even?".to_string(), (vec!["n".to_string()],
                                                EIf(Box::new(EApp(Box::new(EVar("=".to_string())),
                                                                  vec![EVar("n".to_string()),
                                                                       ENum(0)])),
                                                    Box::new(EBool(true)),
                                                    Box::new(EApp(Box::new(EVar("odd?".to_string())),
                                                                           vec![EApp(Box::new(EVar("-".to_string())),
                                                                                     vec![EVar("n".to_string()),
                                                                                          ENum(1)])]))))),
                         ("odd?".to_string(), (vec!["n".to_string()],
                                                EIf(Box::new(EApp(Box::new(EVar("=".to_string())),
                                                                  vec![EVar("n".to_string()),
                                                                       ENum(0)])),
                                                    Box::new(EBool(false)),
                                                    Box::new(EApp(Box::new(EVar("even?".to_string())),
                                                                           vec![EApp(Box::new(EVar("-".to_string())),
                                                                                     vec![EVar("n".to_string()),
                                                                                          ENum(1)])])))))],

                    Box::new(EApp(Box::new(EVar("even?".to_string())),
                                   vec![ENum(5)]))),
               top_r.clone()));

    print!("T ");
    // (letrec ([even?odd? (lambda (b)
    //                        (lambda (n)
    //                           (if (= 0 n)
    //                               b
    //                               ((even?odd? (if b #f #t)) (- n 1)))))])
    //    (let ([even? (even?odd? #t)]
    //          [odd?  (even?odd? #f)])
    //       (even? 5)))
    print(eval(ERec(vec![("even?odd?".to_string(), (vec!["b".to_string()],
						    ELam(vec!["n".to_string()],
							 Box::new(EIf(Box::new(EApp(Box::new(EVar("=".to_string())),
										    vec![EVar("n".to_string()),
											 ENum(0)])),
								      Box::new(EVar("b".to_string())),
								      Box::new(EApp(Box::new(EApp(Box::new(EVar("even?odd?".to_string())),
												  vec![EIf(Box::new(EVar("b".to_string())),
													   Box::new(EBool(false)),
													   Box::new(EBool(true)))])),
										    vec![EApp(Box::new(EVar("-".to_string())),
											      vec![EVar("n".to_string()),
												   ENum(1)])])))))))],
		    Box::new(ELet(vec![("even?".to_string(), EApp(Box::new(EVar("even?odd?".to_string())),
								  vec![EBool(true)])),
				       ("odd?".to_string(), EApp(Box::new(EVar("even?odd?".to_string())),
								 vec![EBool(false)]))],
				  Box::new(EApp(Box::new(EVar("even?".to_string())),
						vec![ENum(5)]))))),
	       top_r.clone()));

    print!("U ");
    // cons
    print(eval(EVar("cons".to_string()), top_r.clone()));

    print!("V ");
    // ()
    print(eval(ENull, top_r.clone()));

    print!("W ");
    // null
    print(eval(EVar("null".to_string()), top_r.clone()));

    print!("X ");
    // (cons 1 ())
    print(eval(EApp(Box::new(EVar("cons".to_string())),
		    vec![ENum(1),
			 ENull]),
	       top_r.clone()));

    print!("Y ");
    // (car (cons 1 ()))
    print(eval(EApp(Box::new(EVar("car".to_string())),
		    vec![EApp(Box::new(EVar("cons".to_string())),
			      vec![ENum(1),
				   ENull])]),
	       top_r.clone()));

    print!("Z ");
    // (cdr (cons 1 ()))
    print(eval(EApp(Box::new(EVar("cdr".to_string())),
		    vec![EApp(Box::new(EVar("cons".to_string())),
			      vec![ENum(1),
				   ENull])]),
	       top_r.clone()));

    print!("AA ");
    // (cons 0 (cons 1 (cons 2 ())))
    print(eval(EApp(Box::new(EVar("cons".to_string())),
		    vec![ENum(0),
			 EApp(Box::new(EVar("cons".to_string())),
			      vec![ENum(1),
				   EApp(Box::new(EVar("cons".to_string())),
					vec![ENum(2),
					     ENull])])]), top_r.clone()));

    print!("AB ");
    //(letrec ([display* (lambda (l) (if (null? l) () {begin (display! (car l)) (display* (cdr l))}))])
    //   (display* (cons 0 (cons 1 (cons 2 null))))
    print(eval(ERec(vec![("display*".to_string(), (vec!["l".to_string()],
                                                   EIf(Box::new(EApp(Box::new(EVar("null?".to_string())),
                                                                     vec![EVar("l".to_string())])),
                                                       Box::new(EVar("null".to_string())),
                                                       Box::new(ESeq(vec![EApp(Box::new(EVar("display!".to_string())),
                                                                               vec![EApp(Box::new(EVar("car".to_string())),
                                                                                         vec![EVar("l".to_string())])]),
                                                                          EApp(Box::new(EVar("display*".to_string())),
                                                                               vec![EApp(Box::new(EVar("cdr".to_string())),
                                                                                         vec![EVar("l".to_string())])])])))))],
		    Box::new(EApp(Box::new(EVar("display*".to_string())),
				  vec![EApp(Box::new(EVar("cons".to_string())),
					    vec![ENum(0),
						 EApp(Box::new(EVar("cons".to_string())),
						      vec![ENum(1),
							   EApp(Box::new(EVar("cons".to_string())),
								vec![ENum(2),
								     ENull])])])]))),
	       top_r.clone()));

    print!("AC ");
    // (letrec ([map (lambda (f l)
    //                  (if (null? l)
    //                      ()
    //                      (cons (f (car l)) (map f (cdr l)))))]
    //
    //     (map display! (cons 0 (cons 1 (cons 2 null)))))
    print(eval(ERec(vec![("map".to_string(), (vec!["f".to_string(), "l".to_string()],
                                              EIf(Box::new(EApp(Box::new(EVar("null?".to_string())),
                                                                vec![EVar("l".to_string())])),
                                                  Box::new(ENull),
                                                  Box::new(EApp(Box::new(EVar("cons".to_string())),
                                                                vec![EApp(Box::new(EVar("f".to_string())),
                                                                          vec![EApp(Box::new(EVar("car".to_string())),
										    vec![EVar("l".to_string())])]),
                                                                     EApp(Box::new(EVar("map".to_string())),
                                                                          vec![EVar("f".to_string()),
                                                                               EApp(Box::new(EVar("cdr".to_string())),
                                                                                    vec![EVar("l".to_string())])])])))))],
		    Box::new(EApp(Box::new(EVar("map".to_string())),
				  vec![EVar("display!".to_string()),
				       EApp(Box::new(EVar("cons".to_string())),
					    vec![ENum(0),
						 EApp(Box::new(EVar("cons".to_string())),
						      vec![ENum(1),
							   EApp(Box::new(EVar("cons".to_string())),
								vec![ENum(2),
								     ENull])])])]))),
	       top_r.clone()));


    print!("AD ");
    // (letrec ([map (lambda (f l)
    //                  (if (null? l)
    //                      ()
    //                      (cons (f (car l)) (map f (cdr l)))))]
    //          [display* (lambda (l)
    //                  (if (null? l)
    //                      ()
    //                      {begin (display! (car l)
    //                             (display* (cdr l))})])
    //    (let ([incr (lambda (n) (+ n 1))]
    //       (display* (map incr (cons 0 (cons 1 (cons 2 null)))))))
    print(eval(ERec(vec![("map".to_string(), (vec!["f".to_string(), "l".to_string()],
                                              EIf(Box::new(EApp(Box::new(EVar("null?".to_string())),
                                                                vec![EVar("l".to_string())])),
                                                  Box::new(ENull),
                                                  Box::new(EApp(Box::new(EVar("cons".to_string())),
                                                                vec![EApp(Box::new(EVar("f".to_string())),
                                                                          vec![EApp(Box::new(EVar("car".to_string())),
										    vec![EVar("l".to_string())])]),
                                                                     EApp(Box::new(EVar("map".to_string())),
                                                                          vec![EVar("f".to_string()),
                                                                               EApp(Box::new(EVar("cdr".to_string())),
                                                                                    vec![EVar("l".to_string())])])]))))),
                         ("display*".to_string(), (vec!["l".to_string()],
                                                   EIf(Box::new(EApp(Box::new(EVar("null?".to_string())),
                                                                     vec![EVar("l".to_string())])),
                                                       Box::new(ENull),
                                                       Box::new(ESeq(vec![EApp(Box::new(EVar("display!".to_string())),
                                                                               vec![EApp(Box::new(EVar("car".to_string())),
                                                                                         vec![EVar("l".to_string())])]),
                                                                          EApp(Box::new(EVar("display*".to_string())),
                                                                               vec![EApp(Box::new(EVar("cdr".to_string())),
                                                                                         vec![EVar("l".to_string())])])])))))],
	Box::new(ELet(vec![("incr".to_string(),
			    ELam(vec!["n".to_string()],
				 Box::new(EApp(Box::new(EVar("+".to_string())),
					       vec![EVar("n".to_string()),
						    ENum(1)]))))],
		      Box::new(EApp(Box::new(EVar("display*".to_string())),
				    vec![EApp(Box::new(EVar("map".to_string())),
					      vec![EVar("incr".to_string()),
						   EApp(Box::new(EVar("cons".to_string())),
							vec![ENum(0),
							     EApp(Box::new(EVar("cons".to_string())),
								  vec![ENum(1),
								       EApp(Box::new(EVar("cons".to_string())),
									    vec![ENum(2),
										 ENull])])])])]))))),
	  top_r.clone()));

    print!("AE ");
    // (letrec ([nums (lambda (n)
    //                   (if (= 0 n)
    //                       null
    //                       (cons n (nums (- n 1)))))]
    //          [fold (lambda (f a l)
    //                   (if (null? l)
    //                       a
    //                       (fold f (f (car l) a) l)))])
    //    (fold + 0 (nums 10)))
    //

    // left as an exercise for the student
}

