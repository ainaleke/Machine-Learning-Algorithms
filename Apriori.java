
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.util.*;


/**
 * The Apriori Algorithm implemented in Java for association rule mining.
 */

public class Apriori {
  private ArrayList<Set<String>> dataSet;
  
  private double minSupport;
  private ArrayList<Set<String>> frequentSet;

  /**
   * Initialization method to import dataset.
   * @param dataSet The list of item set.
   */
  Apriori(ArrayList<Set<String>> dataSet) {
    this.dataSet = dataSet;
  }

  /**
   * Get association rules according to the dataset imported.
   * @param minSupport The minimum support
   * @return List of association rules.
   */
  public ArrayList<AssociationRule> getAssociationRules(double minSupport,double minConfidence) {
    this.minSupport = minSupport;
    this.frequentSet = getFrequentSet();

    return generateRules(minConfidence);
  }

  private ArrayList<Set<String>> getFrequentSet() {
    ArrayList<Set<Set<String>>> frequentItemSetList = new ArrayList<>();

    // 0-Set
    frequentItemSetList.add(null);

    // Get the set that contains all item
    Set<String> allItems = new HashSet<>();
    for (Set<String> transaction : dataSet) {
      for (String item : transaction) {
        allItems.add(item);
        //allItems contains all the unique items in the whole list
      }
    }

    // System.out.printf("AllItems: %s\n", allItems);

    // Get large 1-itemset
    frequentItemSetList.add(new HashSet<>());
    for (String item : allItems) {
      Set<String> oneSet = new HashSet<>();
      oneSet.add(item);
      double support = getSupport(oneSet);
      if (support >= minSupport) {
        frequentItemSetList.get(1).add(oneSet);
      }
    }

    int k = 2;
    while (frequentItemSetList.get(k-1).size() != 0) {
      // System.out.printf("L[k-1]: %s\n", L.get(k-1));
      frequentItemSetList.add(new HashSet<>());

      Set<Set<String>> C = new HashSet<>();

      for (Set<String> eachFrequentItemSet : frequentItemSetList.get(k-1)) {
        for (String string : allItems) {
          if (eachFrequentItemSet.contains(string)) continue;
          Set<String> c = new HashSet<>();
          c.addAll(eachFrequentItemSet);
          c.add(string);
          // System.out.println(c);
          if (C.contains(c)) continue;
          if (!checkSet(c, frequentItemSetList.get(k-1))) continue;
          C.add(c);
        }
      }

      for (Set<String> c : C) {
        if (getSupport(c) < minSupport) continue;
        frequentItemSetList.get(k).add(c);
      }
      k++;
    }

    ArrayList<Set<String>> frequentSet = new ArrayList<>();
    for (int i = 1; i < k; i++) {
      frequentSet.addAll(frequentItemSetList.get(i));
    }
    return frequentSet;
  }

  private boolean checkSet(Set<String> S, Set<Set<String>> L) {
    Set<String> S2 = new HashSet<>();
    S2.addAll(S);

    for (String item : S) {
      S2.remove(item);
      if (!L.contains(S2)) return false;
      S2.add(item);
    }

    return true;
  }

  private double getSupport(Set<String> itemSet) {
    int count = 0;

    for (Set<String> transaction : dataSet) {
      if (transaction.containsAll(itemSet)) {
        count++;
      }
    }
    return (double)count / dataSet.size();
  }

  private ArrayList<AssociationRule> generateRules(double minConfidence) {
    ArrayList<AssociationRule> rules = new ArrayList<>();
    for (Set<String> base : frequentSet) {
      if (base.size() == 1) {continue;}

      double baseSupport = getSupport(base);
      ArrayList<String> baseList = new ArrayList<>(base);

      class Inner {
        void generateRulesDFS(int cur, Set<String> left, Set<String> right) {
          if (cur == baseList.size()) {
            if (left.size() == 0 || right.size() == 0) {
            	return;
            }

            double leftSupport = getSupport(left);
            double rightSupport = getSupport(right);
            if (leftSupport < minSupport || rightSupport < minSupport) {
            	return;
            }
            	
            
           double confidence=baseSupport / leftSupport;
            if(confidence<minConfidence){
            	return;
            }
//            System.out.println("Base support"+baseSupport);
//            System.out.println("left support"+leftSupport);
            AssociationRule rule = new AssociationRule(
                new HashSet<>(left), new HashSet<>(right), baseSupport, confidence);
            rules.add(rule);
          }
          else {
            String ele = baseList.get(cur);
            left.add(ele);
            generateRulesDFS(cur + 1, left, right);
            left.remove(ele);
            right.add(ele);
            generateRulesDFS(cur + 1, left, right);
            right.remove(ele);
          }
        }
      }

      // use depth-first search to generate all subset of base
      Inner dfs = new Inner();
      Set<String> left = new HashSet<>();
      Set<String> right = new HashSet<>();
      dfs.generateRulesDFS(0, left, right);
    }

    return rules;
  }

//  private static void runTest(String[][] input) {
//    ArrayList<Set<String>> dataSet = new ArrayList<>();
//    for (String[] trans : input) {
//      dataSet.add(new HashSet<>(Arrays.asList(trans)));
//    }
//    // System.out.println(dataSet);
//    Apriori apirori = new Apriori(dataSet);
//    ArrayList<AssociationRule> res = apirori.getAssociationRules(0.3);//2.0/9.0
//    for(int i=0;i<res.size();i++){
//    	System.out.println(res.get(i));
//    }
//    
//  }

  private static void runTest(ArrayList<Set<String>> dataSet,double minSupport,double minConfidence) {
	    //ArrayList<Set<String>> dataSet = new ArrayList<>();
	  
	    Apriori apirori = new Apriori(dataSet);
	    ArrayList<AssociationRule> resultList = apirori.getAssociationRules(minSupport,minConfidence);//2.0/9.0);
	    for(int i=resultList.size()-1;i>=0;i--){
//	    	if(resultList.contains(resultList.get(i).left) && resultList.contains(resultList.get(i).right)){
//	    		continue;
//	    	}
	    	System.out.println(resultList.get(i));
	    }
  }

  public static void main(String[] args) throws Exception {
	  
	  Scanner readInput = new Scanner(System.in);
	  System.out.print("Please Enter Minimum Support %: ");
	  double minSupport= readInput.nextDouble();
	  System.out.println();
	  
	  while(minSupport>100 || minSupport<1){
		  if(minSupport>100){
			  System.out.println("Suppport is Greater than 100: ");  
		  }
		  else{
			  System.out.println("Suppport is Less than 1: ");  
		  }
		  
		  System.out.println("Please Enter Support %: ");
		  minSupport= readInput.nextDouble();  
	  }
	  minSupport=minSupport/100;
	  
	  //Get confidence values:
	  
	  System.out.print("Please Enter Minimum Confidence %: ");
	  double minConfidence=readInput.nextDouble();
	  System.out.println();
	  
	  
	  while(minConfidence>100 || minConfidence<1){
		  if(minConfidence>100){
			  System.out.println("Confidence is Greater than 100: ");  
		  }
		  else{
			  System.out.println("Confidence is Less than 1: ");  
		  }
		  
		  System.out.println("Please Enter Confidence %: ");
		  minConfidence= readInput.nextDouble();  
	  }
	  minConfidence=minConfidence/100;
	  
	  
	  System.out.print("Please Enter Database Name %: ");
	  String databaseName=readInput.next();
	  System.out.println();
	  
	  ArrayList<Set<String>> dataSet=readDataSetFile("src/"+databaseName+".txt");
	  System.out.println("\nSupport is: "+minSupport*100 +"%");
	  System.out.println("\nConfidence is: "+minConfidence*100 +"%");
	  System.out.println("\nDatabase Name: "+databaseName);
	  
	  System.out.println("---------------Data Set-------------------------");
	  for(int i=0;i<dataSet.size();i++){
		System.out.println(dataSet.get(i));
	  }
	  System.out.println("\n\n---------------Frequent ItemSets-------------------------");
	  runTest(dataSet,minSupport,minConfidence);
		
  }

public static ArrayList<Set<String>> readDataSetFile(String fileName) {
	ArrayList<Set<String>> transactions=new ArrayList<>();
	try {
			File inputFile=new File(fileName);
			BufferedReader bufferReader=new BufferedReader(new FileReader(inputFile));
			Set<String> transaction;
			String line=null;
			while((line=bufferReader.readLine())!=null)
			{
				if(line.isEmpty())
				{
					continue; //if it encounters an empty line then continue or skip to the next line by continuing with the loop 
				}
			
				//split each line using the whitespace characters(whether they are one or more white space chars between each entry on every line
				String[] eachLine_InArrayForm=line.split(" ");
				 transaction = new HashSet<String>();
				for(String num: eachLine_InArrayForm){
					//transaction.add(Integer.parseInt(num));
					transaction.add(num);
				}
				//if the line is empty, move on to next iteration
				if(transaction.isEmpty()){
					continue;
				}
				//Collections.sort(transaction);
				transactions.add(transaction);
				
				//readInput.close();
			}
			bufferReader.close();
	}
	catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
	}
	return transactions;
  }

}