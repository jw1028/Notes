import java.util.*; 
public class Main{ 
    public static void main(String[] args) { 
        Scanner scan = new Scanner(System.in); 
        while(scan.hasNextInt()) { 
            int n = scan.nextInt(); 
            long[] array = new long[3*n]; 
            for(int i = 0;i < array.length;i++) { 
                array[i] = scan.nextLong(); 
            }
            Arrays.sort(array); 
            long sum = 0; 
            for (int i = 0; i < n; i++) { 
                sum += array[array.length-(2*(i+1))]; 
            } 
            System.out.println(sum); 
        } 
    }
}
