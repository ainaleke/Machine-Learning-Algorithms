import java.text.DecimalFormat;
import java.util.Set;

public class AssociationRule implements Comparable<AssociationRule> {
	public final Set<String> left;
	public final Set<String> right;
	public final double support;
	public final double confidence;
	
	AssociationRule(Set<String> left, Set<String> right, double support, double confidence) {
	    this.left = left;
	    this.right = right;
	    this.support = support;
	    this.confidence = confidence;
	}

	public int compareTo(AssociationRule other) {
		return Double.compare(other.support, support);
	}

  	public String toString() {
	   DecimalFormat df = new DecimalFormat("#.00");
	    return left +" =>" + right + "  Support: "+df.format(support * 100)+"%,   Confidence: "+ df.format(confidence * 100)+"%";
	}
  	public Set<String> getLeft() {
		return left;
	}

	public Set<String> getRight() {
		return right;
	}
	public double getSupport() {
		return support;
	}
	public double getConfidence() {
		return confidence;
	}

}
