package tokenizers;
import java.io.*;
import java.util.*;

import edu.stanford.nlp.ling.CoreAnnotations.LemmaAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.SentencesAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.TokensAnnotation;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.util.CoreMap;
import edu.stanford.nlp.util.Pair;
import edu.stanford.nlp.util.StringUtils;

public  class tokens {

    protected StanfordCoreNLP pipeline;

    public tokens() {
        // Create StanfordCoreNLP object properties, with POS tagging
        // (required for lemmatization), and lemmatization
        Properties props;
        props = new Properties();
        props.put("annotators", "tokenize, ssplit, pos, lemma");

        this.pipeline = new StanfordCoreNLP(props);
    }

    public Integer tokenize(String documentText)
    {
    	Integer total=0;
    	Map<String,Integer> mp = new HashMap<String,Integer>();
    	Map<String,Integer> bimp = new HashMap<String,Integer>();
    	Map<String,Integer> trimp = new HashMap<String,Integer>();
    	
		//System.out.print(documentText);
        List<String> lemmas = new LinkedList<String>();
        // Create an empty Annotation just with the given text
        Annotation document = new Annotation(documentText);
        // run all Annotators on this text
        this.pipeline.annotate(document);
        // Iterate over all of the sentences found
        List<CoreMap> sentences = document.get(SentencesAnnotation.class);
        System.out.println("total_sentences : "+sentences.size());
        for(CoreMap sentence: sentences) {
            // Iterate over all tokens in a sentence
        	List<CoreLabel> labels=sentence.get(TokensAnnotation.class);
        	
        	StringUtils s=null;
        	Collection<String> grams=s.getNgramsFromTokens(labels,1,1);
        	Collection<String> bigrams=s.getNgramsFromTokens(labels,2,2);
        	Collection<String> trigrams=s.getNgramsFromTokens(labels,3,3);
        	
        	for(String x:grams)
        		{total++;
                if(mp.containsKey(x))
					mp.put(x, mp.get(x) + 1);
			   else
					mp.put(x,1);
        		
        		}
        	
        	for(String x:bigrams)
    		{
            if(bimp.containsKey(x))
            	bimp.put(x, bimp.get(x) + 1);
		   else
			   bimp.put(x,1);
    		
    		}
        	for(String x:trigrams)
    		{
            if(trimp.containsKey(x))
            	trimp.put(x, trimp.get(x) + 1);
		   else
			   trimp.put(x,1);
    		
    		}
        	
        	
        	
        	
        }
        printresult p=new printresult();
      
   Integer a=total;
 
        p.print(mp,"unigram.txt",a,90);
        p.print(bimp,"bigram.txt",a,80);
      
        p.print(trimp,"trigram.txt",a,70);
return total;  
    }
    
    public List<String> readfolder() // reading files from the directory one by one ...........
    {   String path="C:\\Users\\Ravindra\\Desktop\\ISI_Project\\pos";  // path of the input directory
    	File folder = new File(path);
    	File[] listOfFiles = folder.listFiles();
        List<String> l=new LinkedList<String>();
    	for (File file : listOfFiles) {
    	    if (file.isFile()) {
    	        l.add(path+"\\"+file.getName());
    	    }
    	}
    	
    	return l;
    }
    

    private List<String> readFile( List<String> files ) throws IOException {
    	List<String> l=new LinkedList<String>();
    	for(String file:files)
        {BufferedReader reader = new BufferedReader( new FileReader (file));
        String         line = null;
        StringBuilder  stringBuilder = new StringBuilder();
        String         ls = System.getProperty("line.separator");
        

        try {
            while( ( line = reader.readLine() ) != null ) {
                stringBuilder.append( line );
                stringBuilder.append( ls );
            }
  //System.out.println(stringBuilder.toString());
            l.add( stringBuilder.toString());
        } finally {
            reader.close();}
        }
    	return l;
    }
   
   
    
	public static void main(String[] args) throws IOException {
       System.out.println("starting....");
      
      tokens tk=new tokens();
       String path="input_corpus.txt";
       List<String> l;
       l=tk.readfolder();
       
      l=tk.readFile(l);
       // heuristic h=new heuristic();
        sentiment1 s1=new sentiment1();
        s1.sentiment_analysis(l);
       // List<String> s=h.sentences(text);
       // List<String> unigrams=h.alltokens(s);
       //// System.out.println("total_sen_heu="+s.size());
       // System.out.println("total words="+unigrams.size());
       // Integer t=tk.tokenize(text);
        
      //  lemmatizer lem = new lemmatizer();
      //  lem.lemmatize(text,t);
        
    
     
 //   h.ngrams(unigrams);
    
  //   h.ngrams_lemmatized(unigrams);
     
  	   
        
       
      
    }

}
