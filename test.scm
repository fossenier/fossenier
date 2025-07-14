(display


 (let ([i 1])

    (let ([f (lambda (x) (+ x i))])

      (let ([i 2])
      
         (f 3))))


)