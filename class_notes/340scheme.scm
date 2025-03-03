#lang racket


// Factorial recursion example


(define fact
    (lambda (i)
        (if (< i 2)
            1
            (* i (fact (- i 1))))))

(fact 3)



// Functions on the fly


((lambda (x) (+ x 1)) 4)

// (lambda (x) (+ x 1)) builds a function
// 4 passses it

(if #t      // EIf( EBool(true),
    4       //      ENum(4),
    5)      //      ENum(5))






(let ([fact (lambda(n)
                     (if (< n 2)
                         1
                         (* nzzzzzzzz (fact (- n 1)))))])
      (fact 5))