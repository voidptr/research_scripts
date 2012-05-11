for i in *_??????/; 
  do echo $i; 
  cd $i; 
  gunzip *.gz; 
  cd data; 
  gunzip *.gz;
  cd phenotype;
  for j in *_/;
    do cd $j;
    echo $j;
    gunzip *.gz;
    cd ../
  done;
  cd ../;
  cd ../../; 
done;
