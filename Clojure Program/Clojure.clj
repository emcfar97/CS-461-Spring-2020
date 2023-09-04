(defn log2 [n] (/ (Math/log n) (Math/log 2)))

(defn entropy [xs]
  
  (let [freqs (vals (frequencies xs))
        cnt (reduce + freqs)
        calc #(let [p (double (/ % cnt))]
                (* p (log2 p)))]
    (reduce - 0 (pmap calc freqs))
    )
  )

(defn file []
  (slurp "School\\4.Spring 2020\\Clojure Program\\WarAndPeace.txt")
  )

(defn split-text [text step]
  
  (loop [tail text result []]
    (if (empty? tail)
      result
      (let [len (min step (count tail))]
        (recur (subs tail len)
               (conj result (subs tail 0 len))
               )
        )
      )
    )
  )

(defn timeit [threads]
  (print threads " threads\n")
  (loop [i 1]
    (when (< i 4)
      (time (print((entropy (split-text (file) i)))))
      (recur (inc i))
      )
    )
  )

(timeit 1)