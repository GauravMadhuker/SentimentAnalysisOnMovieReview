package tokenizers;
import java.io.*;
import java.util.*;
import java.lang.*;

import edu.stanford.nlp.ling.CoreAnnotations.LemmaAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.SentencesAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.TokensAnnotation;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.util.CollectionUtils;
import edu.stanford.nlp.util.CoreMap;
import edu.stanford.nlp.util.Pair;
import edu.stanford.nlp.util.StringUtils;
import edu.stanford.nlp.parser.common.ParserGrammar;

public class heuristic {
	
	 protected StanfordCoreNLP pipeline;
	 
	 public heuristic()
	 {
		  Properties props;
	        props = new Properties();
	        props.put("annotators", "tokenize, ssplit, pos, lemma");

	        this.pipeline = new StanfordCoreNLP(props);
	 }
	 public List<String> sentences(String text)
	 {
		 String s="";
		 List<String> l=new LinkedList<String>();
		 for(int i=0;i<text.length();i++)
		 {
			 if(text.charAt(i)=='?'||text.charAt(i)=='!'||text.charAt(i)=='.')
				 {l.add(s);s="";}
			 else 
				 {
				
				   s=s+text.charAt(i);
				 }
		 }
		 return l;
	 }
		
	
	public List<String> alltokens(List<String> sentences)
	{
		List<String> l= new LinkedList<String>();
		for(String s:sentences)
		{ //System.out.println(s);
			String[] temp=s.split("-|\\s+|\\.|:|\\n");
			for(String s1:temp)
				if(!(s1.equals("")))
				    l.add(s1);
		}
		
		return l;
	}
	
	
	public void ngrams(List<String> lemmas)
	{  
		int total=lemmas.size();
	Map<String,Integer> mp = new HashMap<String,Integer>();
	Map<String,Integer> bimp = new HashMap<String,Integer>();
	Map<String,Integer> trimp = new HashMap<String,Integer>();
		 List < List<String> > unigram= CollectionUtils.getNGrams(lemmas, 1, 1);
	        List < List<String> > bigram= CollectionUtils.getNGrams(lemmas, 2, 2);
	        List < List<String> > trigram= CollectionUtils.getNGrams(lemmas, 3, 3);
	        for(List<String> l:unigram)
	        {
	        	for(String x:l)
	        		if(mp.containsKey(x))
						mp.put(x, mp.get(x) + 1);
				   else
						mp.put(x,1);
	        }
	        
	        for(List<String> l:bigram)
	        {  String s="";
	        	for(String x:l)
	        		s=s+x+" ";
	        		if(bimp.containsKey(s))
						bimp.put(s, bimp.get(s) + 1);
				   else
						bimp.put(s,1);
	        }
	        for(List<String> l:trigram)
	        {  String s="";
	        	for(String x:l)
	        		s=s+x+" ";
	        		if(trimp.containsKey(s))
	        			trimp.put(s, trimp.get(s) + 1);
				   else
					   trimp.put(s,1);
	        }
	        printresult p=new printresult();
	       // System.out.println("total="+total);
	        Integer a=total;
	       /// System.out.println("total ="+a);
	            p.print(mp,"unigram_heuristic.txt",a,90);
	             
	             p.print(bimp,"bigram_heuristic.txt",a,80);
	           
	           
	             p.print(trimp,"trigram_heuristic.txt",a,70);
	        
	        
	       
	}
	public void ngrams_lemmatized(List<String> words)
	{ int total=words.size();
	 String text="";
	 for(String w:words)
		 text=text+w+" ";
	 
	
		Map<String,Integer> mp = new HashMap<String,Integer>();
    	Map<String,Integer> bimp = new HashMap<String,Integer>();
    	Map<String,Integer> trimp = new HashMap<String,Integer>();
    	
    	
        List<String> lemmas = new LinkedList<String>();
        // Create an empty Annotation just with the given text
        Annotation document = new Annotation(text);
        // run all Annotators on this text
        
        this.pipeline.annotate(document);
        // Iterate over all of the sentences found
        List<CoreMap> sentences = document.get(SentencesAnnotation.class);
        for(CoreMap sentence: sentences) {
            // Iterate over all tokens in a sentence
            for (CoreLabel token: sentence.get(TokensAnnotation.class)) {
                // Retrieve and add the lemma for each word into the
                // list of lemmas
                lemmas.add(token.get(LemmaAnnotation.class));
            }
        }
        List < List<String> > unigram= CollectionUtils.getNGrams(lemmas, 1, 1);
        List < List<String> > bigram= CollectionUtils.getNGrams(lemmas, 2, 2);
        List < List<String> > trigram= CollectionUtils.getNGrams(lemmas, 3, 3);
        for(List<String> l:unigram)
        {
        	for(String x:l)
        		if(mp.containsKey(x))
					mp.put(x, mp.get(x) + 1);
			   else
					mp.put(x,1);
        }
        
        for(List<String> l:bigram)
        {  String s="";
        	for(String x:l)
        		s=s+x+" ";
        		if(bimp.containsKey(s))
					bimp.put(s, bimp.get(s) + 1);
			   else
					bimp.put(s,1);
        }
        for(List<String> l:trigram)
        {  String s="";
        	for(String x:l)
        		s=s+x+" ";
        		if(trimp.containsKey(s))
        			trimp.put(s, trimp.get(s) + 1);
			   else
				   trimp.put(s,1);
        }
        printresult p=new printresult();
       // System.out.println("tatal="+total);
        Integer a=total;
       /// System.out.println("tatal ="+a);
            p.print(mp,"unigram_lemmatised_heuristic.txt",a,90);
              p.print(bimp,"bigram_lemmatised_heuristic.txt",a,80);
           
              p.print(trimp,"trigram_lemmatised_heuristic.txt",a,70);
        
        
	}
	

}
