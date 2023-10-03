# Read_card_py_GIT
print ans_card_60_thin_math.pdf or ans_card_60_thin_english.pdf on paper
scan paper to computer
select file then scan
the result will store in  result/out.xlsx
Copying result/out.xlsx/sheet1 to OUT.xlsm/sheet1
enable excel VBA

improt ans in OUT.xlsm/sheet2 col3

單選題 is multiple choice questions(one answer)
ex : question ans A  student ans B -> 0
ex : question ans A  student ans A -> 10

多選題 is multiple choice questions(two or more answer and every choice ratio is set on sheet2/B64)
ratio 0.4(sheet2/B64)
ex : question ans | score | student ans |  
               AB      10              C  -> 0  (error on ABC)
               AB      10              A  -> 6  (error on B)
               AB      10              B  -> 6  (error on A)
               AB      10             AB  -> 10 
               AB      10       (no ans)  -> 2  (error on AB)
               
ratio 0.2(sheet2/B64)
ex : question ans | score | student ans |  
               AB      10              C  -> 4  (error on ABC)
               AB      10              A  -> 8  (error on B)
               AB      10              B  -> 8  (error on A)
               AB      10             AB  -> 10 
               AB      10       (no ans)  -> 6  (error on AB)
               
                  
選填題 is Optional questions(need all ans correct will have score)
ex : question ans | score | student ans |  
                1       0              1
                2       0              1
                1      10              1 -> 0
  
                1       0              1
                2       0              2
                1      10              1 -> 10
