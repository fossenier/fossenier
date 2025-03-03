type SSym = String;

type SResult = Result<SVal, String>;

#[derive (Clone)]

// SVal ::= String
//       |  Number
//       |  Bool
// ,...

// This was removed or moved???

// type Prim0 = dyn Fn() -> SResult;
// type Prim1 = dyn Fn(SVal) -> SResult;
// type Prim2 = dyn Fn(Sval, SVal) -> SResult;
// type Print = dyn (SVal) -> ();

enum SVal {
    VStr ( String ),        // SVal::VStr
    Vnum ( i32 ),
    VBool ( bool),

    VNull,                  // dotted pairs
    VPair ( Box<SVal>,
           Box<SVal> ),

    VFun ( Vec<SSym>,
           Box<SExp>,
           Box<SEnv> ),

    VPrim ( SSym )
        

    // also removed

    // VPrim0 ( Box<Prim0> ),
    // VPrim1 ( Box<Prim1> ),
    // VPrim2 ( Box<Prim2> ),
    // VPrim3 ( Box<Print> ),
}

// gap

enum SEnv {
    REmpty,
    RScope ( Vec<(SSym, SVal)>,
             Box<SEnv> ),
    RRec ( Vec<(SSym,
                (Vec<SSym>, SExp))>,
         Box<SEnv> )
}

// gap


use SVal::*;

enum SExp {
    Estr ( String ),        // "abc"
    ENum ( i32 ),           // 123
    EBool ( bool ),         // #t #Fn

    EIf ( Box<SExp>,        // (if  .Test.
          Box<SExp>,        //      .Consequent.
          Box<SExp> ),      //      .Alternate )
    
    // variables and bindings
    Evar ( SSym ),          // .Id.
    ELet ( Vec<(SSym, SExp)>,       // (let ([.Id. .Exp.] ...)
          Box<SExp> ),      //      .Body. )
    ERect ( Vec<(SSym,                  // (letrec ([.Id. (lambda (.Id. ...) .Exp.)]
                 (Vec<SSym>, SExp))>,  //          ...)
                 Box<SExp> ),      //      .Body. )



    // ELet ( Vec<SSym>,       // (let ([.id. .Exp.]
    //        Vec<SExp>,       //      ...)
    //        Box<SExp> ),     //      .Body. )
    // EVar ( SSym ),          // .id.

    // ELetRec ( Vec<SSym>,        // (letrec ([.id. (lambda (.id. ..     Here??
    //          Vec<SExp>,         //          ...)
    //          Box<SExp> ),       //        .Body. 

    // sequencing
    ESeq ( Vec<SExp> ),             // (begin .Exp. ...)
    ENull,                          // ()    -- (begin ) is INVALID syntax

    // functions
    ELam ( Vec<SSym>,               // (lambda (.Id. ...))
          Box<SExp> ),              //          .Exp. )
    EApp ( Box<SExp>,               // (.Exp.
           Vec<SExp> ),             //          ...)
    
    // ELam ( Vec<SSym>,           //(lambda (.id. ...)
    //         Box<SExp> ),        //   .Exp. )
    // EApp ( Vec<Box<SExp>> ),    // (.Exp.  ...)
}

use SExp::*;

enum SDecl {
    TDef ( SSym,                // (define .id. .Exp.)
           SExp ),
}

use SDecl::*;

enum SProg {
    SPrg ( Vec<SDecl>,
           SExp ),
}

use SProg::*;

enum SBind {
    RBind ( SSym,
            SVal ),
}

// break

use std::iter::*;

fn eval(e : SExp, r : SEnv) -> SResult {
    match e {
        EStr(s) => Ok(Vstr(s)),
        ENum(z) => Ok(Vnum(z)),
        EBool(b) => Ok(VBool(b)),

    EIf(t, c, a) => match evall(*t, r) {
        Ok(VBool(true)) => eval(*c, r),
        Ok(VBool(false)) => eval(*a, r),
        _               => Err("non-boolean test".to_string()),
    },

    EVar(y) => lookup(y, r),
    Elet(yes, b) => { let yvs = evals(yes, &r);
                      fn yv_ok((_, v) : (SSym, SResult)) -> bool {
                        match v {
                            Ok(v) => (y.clone(), v.clane()),
                            Err(_) => panic!("Err value after seeing none")
                        }
                      }
                      fn yv_unwrap((y, v) : &(SSym, SResult)) -> (SSym, Sval) {
                        match v {
                            Ok(v) => (y.clone(), v.clone()),
                            Err(_) => panic!("Err value after seeing none")
                        }
                      }
                      if yvs.iter().fold(true, |b, yv| b && yv_ok(yv.clone())) {
                        eval(*b, RScope(yvs.iter().map(yv_unwrap).collect(), Box::new(r.clone())))
                      } else {
                        Err("arguments bad".to_string())
                      }
    }


    // ELet(yes, b) => match evals(es, r) {
    //     Ok(vs) => match bind(ys, vs) {
    //         Some(yvs) => eval(*b, RScope(yvs, Box::new(r))),
    //         None => Err("arguments bad".to_string()),
    //     },
    //     Err(s) => Err(s),
    // },


    ERec(ys, yses, b) => match bind(ys, yses) {
        Some(yysess) => eval(*b, RRec(yysess, Box::new(r))),
        None => Err("recursive arguments bad".to_string()),
    },

    ESeq(es) => match evals(es, r) {
        Ok(vs) => match vs.last() {
            Some(_v) => Ok(*_v),
            //gap
        }
    }
    //gap
}})










// Examples

// (let ([a 1] [b 2]) a)
// identical to
// ((lambda (a b) a) 1 2)
print(eval(ELet(vec![("a".to_string(), ENum(1))
                     ("b".to_string(), ENum(2))],
                Box::new(EVar("a".to_string()))), REmpty));

// Question, is this also permissible?
// (let ([incr (lambda (n) (+ n 1))]))
//        (incr 2)
// Apparently yes

// (let [a 1] [b 2]) (let ([a b] [c 3]) a))
print(eval(ELet(vec![("a".to_string(), ENum(1))
                     ("b".to_string(), ENum(2))],
                Box::new(ELet(vec![("a".to_string(), EVar("b".to_string()))
                                   ("c".to_string(), ENum(3))],
                              Box::new(EVar("a".to_string()))))), REmpty));

// (let ([a 1] [b 2]) b)
print(eval(ELet(vec![("a".to_string(), ENum(1))
                     ("b".to_string(), ENum(2))],
                Box::new(EVar("b".to_string()))), REmpty));

// (let ([i 1])
//    (let ([f (lambdo (x) (+ x i))])
//       (let ([i 2])
//          (f 3))))
print(eval(ELet(vec![("i".to_string(), ENum(1))],
                Box::new(ELet(vec![("f".to_string(), ELam(vec!["x".to_string()],
                                                            Box::new(EApp(Box::new(EVar("+".to_string())),
                                                                          vec![EVar("x".to_string()), EVar("i".to_string())])))]),
                              Box::new(ELet(vec![("i".to_string(), ENum(2))],
                                            Box::new(EApp(Box::new(EVar("f".to_string())),
                                                          vec![ENum(3)]))))))), REmpty));