type SSym = String;

type SResult = Result<SVal, String>;

type Prim0 = dyn Fn() -> SResult;
type Prim1 = dyn Fn(SVal) -> SResult;
type Prim2 = dyn Fn(Sval, SVal) -> SResult;
type Print = dyn (SVal) -> ();

// gap

enum SVal {
    VStr ( String ),        // SVal::VStr
    Vnum ( i32 ),
    VBool ( bool),

    VList ( SList ),

    VFun ( LinkedList<SSym>,
           SExp,
           SEnv ),
        
    VPrim0 ( Box<Prim0> ),
    VPrim1 ( Box<Prim1> ),
    VPrim2 ( Box<Prim2> ),
    VPrim3 ( Box<Print> ),
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