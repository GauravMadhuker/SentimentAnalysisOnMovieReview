package tokenizers;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.PrintStream;
import java.util.Arrays;
import java.util.Comparator;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Properties;

import edu.stanford.nlp.ling.CoreAnnotations.LemmaAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.SentencesAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.TokensAnnotation;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.util.CollectionUtils;
import edu.stanford.nlp.util.CoreMap;

public class lemmatizer {

    protected StanfordCoreNLP pipeline;

    public lemmatizer() {
        // Create StanfordCoreNLP object properties, with POS tagging
        // (required for lemmatization), and lemmatization
        Properties props;
        props = new Properties();
        props.put("annotators", "tokenize, ssplit, pos, lemma");

      
        this.pipeline = new StanfordCoreNLP(props);
    }

    public void lemmatize(String documentText,Integer total)
    {
    	Map<String,Integer> mp = new HashMap<String,Integer>();
    	Map<String,Integer> bimp = new HashMap<String,Integer>();
    	Map<String,Integer> trimp = new HashMap<String,Integer>();
    	
    	
        List<String> lemmas = new LinkedList<String>();
        // Create an empty Annotation just with the given text
        Annotation document = new Annotation(documentText);
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
            p.print(mp,"unigram_lemmatised.txt",a,90);
              p.print(bimp,"bigram_lemmatised.txt",a,80);
           
             p.print(trimp,"trigram_lemmatised.txt",a,70);
        
        
       
    }

   
    

}

