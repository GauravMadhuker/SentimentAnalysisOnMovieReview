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

import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.ling.CoreAnnotations.LemmaAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.SentencesAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.TokensAnnotation;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.sentiment.SentimentCoreAnnotations;
import edu.stanford.nlp.util.CollectionUtils;
import edu.stanford.nlp.util.CoreMap;



public class sentiment1 {
	 protected StanfordCoreNLP pipeline;
	 int tp=0;
	 int fp=0;
	 int fn=0;

	public sentiment1() {
                       // Create StanfordCoreNLP object properties, with POS tagging
                       // (required for lemmatisation), parsing and sentiment analysis
        Properties props;
        props = new Properties();
        props.put("annotators", "tokenize, ssplit, pos, lemma,parse,sentiment");
        this.pipeline = new StanfordCoreNLP(props);
    }
	
	public void sentiment_analysis(List<String> l)
	{  int c=0;
	double x=0;
	int sum[]=new int[200],a=0;
		for(String text :l)
		{
			c++;
			
		a=0;
		Annotation annotation = pipeline.process(text); // staring CoreNlp pipeline
		List<CoreMap> sentences = annotation.get(CoreAnnotations.SentencesAnnotation.class);
		// using sentence annotators
		// finding sentiment of each sentence using sentiment annotator 
		for (CoreMap sentence : sentences) {
		  String sentiment = sentence.get(SentimentCoreAnnotations.SentimentClass.class);
		 // System.out.println(sentiment);
		 
		if(sentiment.equals("Negative"))
			sum[a]=-1;
		else if(sentiment.equals("Neutral"))
			sum[a]=0;
		else if(sentiment.equals("Very negative"))
			sum[a]=-2;
		else if(sentiment.equals("Very positive"))
			sum[a]=2;
		else
			sum[a]=1;
	a++;
		//  System.out.println(sentiment + "\t"+sentence);
		}
		int sum1=0;int d=0;int b=0;    
		for(int i=0;i<a;i++)
			{sum1=sum1+sum[i];d++;}
		/*                                //  heuristic to classify the sentiment of the document
			for(int i=a;i>10;i--)
				{b++;
				sum1=sum1+sum[i];
			if(b==10)
				break;
				}		*/
		
		x=sum1/(double)(d+b);
		
		String s="";
		if(x<-0.5)
			s="Negative";
	
		else
			s="Positive";
	
		System.out.println( "sentiment of the file no.\t" +c +" : "+ s );
		if(s.equals("Positive"))
			tp++;
		else if(s.equals("Negative"))
			fp++;
		
		
		}
		System.out.println("pos = "+tp+"  "+"neg  ="+fp);
		
	}

}
