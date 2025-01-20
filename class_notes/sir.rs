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

use SVal::*;

enum SExp {
    Estr ( String ),        // "abc"
    ENum ( i32 ),           // 123
    EBool ( bool ),         // #t #Fn

    EIf ( Box<SExp>,        // (if  .Test.
          Box<SExp>,        //      .Consequent.
          Box<SExp> ),      //      .Alternate )
    
    ELet ( Vec<SSym>,       // (let ([.id. .Exp.]
           Vec<SExp>,       //      ...)
           Box<SExp> ),     //      .Body. )
    EVar ( SSym ),          // .id.

    ELetRec ( Vec<SSym>,        // (letrec ([.id. (lambda (.id. ..     Here??
             Vec<SExp>,         //          ...)
             Box<SExp> ),       //        .Body. 
    
    ELam ( Vec<SSym>,           //(lambda (.id. ...)
            Box<SExp> ),        //   .Exp. )
    EApp ( Vec<Box<SExp>> ),    // (.Exp.  ...)
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

fn eval(e : SExp, r : SEnv) -> SResult {
    match e {
        EStr(s) => Ok(Vstr(s)),
        ENum(z) => Ok(Vnum(z)),
        EBool(b) => Ok(VBool(b)),

    EIf(t, c, a) => match evall(t, r) {
        Ok(VBool(true)) => eval(*c, r),
        Ok(VBool(false)) => eval(*a, r),
        _               => Err("non-boolean test".to_string()),
    },

    EVar(y) => lookup(y, r),
    ELet(ys, es, b) => match evals(es, r) {
        Ok(vs) => match bind(ys, vs) {
            Some(yvs) => eval(*b, RScope(yvs, Box::new(r))),
            None => Err("arguments bad".to_string()),
        },
        Err(s) => Err(s),
    },
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