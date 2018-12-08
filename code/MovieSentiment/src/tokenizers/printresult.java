package tokenizers;
import java.io.*;
import java.util.*;
public class printresult {
	
	
	
	public void print(Map<String,Integer> mymap,String path,Integer t ,int m)
    { int t2=t*m/100;
    	PrintStream out=null;
		try {
			out = new PrintStream(new FileOutputStream(path));
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		System.setOut(out);
    	
    	Object[] a = mymap.entrySet().toArray();
    Arrays.sort(a, new Comparator() {
        public int compare(Object o1, Object o2) {
            return ((Map.Entry<String, Integer>) o2).getValue().compareTo(
                    ((Map.Entry<String, Integer>) o1).getValue());
        }
    });
    Integer t1=0,count=0;
    for (Object e : a) {
    	if(t1<t2)
    	{t1=t1+((Map.Entry<String, Integer>) e).getValue();count++;}
    	
    	
        System.out.println(((Map.Entry<String, Integer>) e).getKey() + " : "
                + ((Map.Entry<String, Integer>) e).getValue());
    } 
    System.out.println("\n\n Total words in the corpus = "+t);
    System.out.println("required items to cover "+ m +" percent of the corpus = " + count);
    
    
    }

}
