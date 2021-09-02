
# 三角形最小路径和
[题目链接：https://leetcode-cn.com/problems/triangle/](https://leetcode-cn.com/problems/triangle/)

```cpp
//自底向上
class Solution {
    public int minimumTotal(List<List<Integer>> triangle) {
        int n = triangle.size();
    if (triangle == null || n == 0){
            return 0;
        }
        // 加1可以不用初始化最后一层
        int[][] f = new int[n + 1][n + 1];

        for (int i = n-1; i>=0; i--){
            List<Integer> cur = triangle.get(i);
            for(int j = 0 ; j < cur.size(); j++){
                f[i][j] = Math.min(f[i+1][j], f[i+1][j+1]) + cur.get(j);
            }
        }
        return f[0][0];
    }
}

class Solution {
    public int minimumTotal(List<List<Integer>> triangle) {
        int n = triangle.size();
        // dp[i][j] 表示从点 (i, j) 到底边的最小路径和。
        int[][] f = new int[n + 1][n + 1];
        // 从三角形的最后一行开始递推。
        for (int i = n - 1; i >= 0; i--) {
            for (int j = 0; j <= i; j++) {
                f[i][j] = Math.min(f[i + 1][j], f[i + 1][j + 1]) + triangle.get(i).get(j);
            }
        }
        return f[0][0];
    }
}
```
# 连续子数组的最大和
[https://leetcode-cn.com/problems/lian-xu-zi-shu-zu-de-zui-da-he-lcof/](https://leetcode-cn.com/problems/lian-xu-zi-shu-zu-de-zui-da-he-lcof/)

```java
class Solution {
    public int maxSubArray(int[] nums) {
        if(nums == null || nums.length == 0) {
            return -1;
        }
        int ret = nums[0];
        for(int i = 1; i < nums.length; i++) {
            nums[i] += Math.max(nums[i - 1], 0);
            ret = Math.max(ret, nums[i]);
        }
        return ret;
    }
}
```

# 最长增长子序列
[题目连接：https://leetcode-cn.com/problems/longest-increasing-subsequence/](https://leetcode-cn.com/problems/longest-increasing-subsequence/)
```cpp
class Solution {
    public int lengthOfLIS(int[] nums) {
        if(nums == null || nums.length == 0) return 0;
        int n = nums.length ;
        int[] f = new int[n + 1];
        int ret = 0;
        for(int i = 0; i <= n - 1; i++) {
            f[i] = 1;
            for(int j = 0; j < i; j++) {
                if(nums[j] < nums[i]) {
                    f[i] = Math.max(f[i] , f[j] + 1);
                }
            }  
             ret = Math.max(ret, f[i]);  
        }
        return ret;
    }
}
//dp + 二分
class Solution {
    public int lengthOfLIS(int[] nums) {
        if(nums == null || nums.length == 0) return 0;
        int n = nums.length;
        //q存储所有不同长度下上升子序列结尾的最小值
        int[] q = new int[n + 1];
        int len = 0;
        for(int i = 0; i < n; i ++ )
        {
            int l = 0, r = len;
            while (l < r)
            {
                int mid = l + r + 1 >> 1;
                if (q[mid] < nums[i]) l = mid;
                else r = mid - 1;
            }
            len = Math.max(len, r + 1);
            q[r + 1] = nums[i];
        }
        return len;
    }
}
```
# 最长公共子串

```java
//最大值
 public static int func(String s1, String s2) {
        int n = s1.length(), m = s2.length();
        int[][] f = new int[n + 1][m + 1];
        int max = 0;
        for(int i = 1; i <= n; i++) {
            for(int j = 1; j <= m; j++) {
                if(s1.charAt(i - 1) == s2.charAt(j - 1)) {
                    f[i][j] = Math.max(f[i - 1][j - 1] + 1, f[i][j]);
                    if(f[i][j] > max) {
                        max = f[i][j];
                    }
                }
            }
        }
        return max;
    }
    //求结果
    public static String func2(String s1, String s2) {
        int n = s1.length(), m = s2.length();
        int[][] f = new int[n + 1][m + 1];
        int max = 0, end = 0;
        for(int i = 1; i <= n; i++) {
            for(int j = 1; j <= m; j++) {
                if(s1.charAt(i - 1) == s2.charAt(j - 1)) {
                    f[i][j] = Math.max(f[i - 1][j - 1] + 1, f[i][j]);
                    if(f[i][j] > max) {
                        max = f[i][j];
                        end = i;
                    }
                }
            }
        }
        return s1.substring(end - max, end);
    }
```

# 最长公共子序列

```cpp
class Solution {
    public int longestCommonSubsequence(String text1, String text2) {
    int n = text1.length(), m = text2.length();
        int[][] f = new int[n + 1][m + 1];
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= m; j++) {
                if (text1.charAt(i - 1) != text2.charAt(j - 1)) {
                    f[i][j] = Math.max(f[i - 1][j], f[i][j - 1]);
                }else {
                    f[i][j] = Math.max(f[i][j], f[i - 1][j - 1] + 1);
                }
            }
        }
        return f[n][m];
    }
}
```
# 最长回文串

```java
    public static boolean isHuiWen(String s) {
        if(s == null ||s.length() == 0) {
            return false;
        }
        int i = 0, j = s.length() - 1;
        while(i < j) {
            if(s.charAt(i) != s.charAt(j)) {
                return false;
            }
            i++;
            j--;
        }
        return true;
    }
    //最长回文长度
    public static int func(String s) {
        // write code here
        int n = s.length();
        int ret = 0;
        for(int i = 0; i < n; i++) {
            for(int j = i + 1; j <= n; j++) {
                if(isHuiWen(s.substring(i, j))) {
                    if(ret < j - i) {
                        ret  = j - i;
                    }
                }
            }
        }
        return ret;
    }
	//最长回文的字符串
    public static String func2(String s) {
        // write code here
        int n = s.length();
        int max = 0, end = 0;
        for(int i = 0; i < n; i++) {
            for(int j = i + 1; j <= n; j++) {
                if(isHuiWen(s.substring(i, j))) {
                    if(max < j - i) {
                        max  = j - i;
                        end = j;
                    }
                }
            }
        }
        return s.substring(end - max, end);
    }
```

# 最长回文序列

```java
public static int func3(String s) {
        if(s == null || s.length() == 0) {
            return 0;
        }
        int n = s.length();
        int[][] f = new int[n + 1][n + 1];
        for(int i = 1; i <= n; i++) {
            for(int j =1; j <= n; j++) {
                if(s.charAt(i - 1) != s.charAt(n - j)) {
                    f[i][j] = Math.max(f[i - 1][j], f[i][j -1]);
                }else {
                    f[i][j] = Math.max(f[i - 1][j - 1] + 1, f[i][j]);
                }
            }
        }
        return f[n][n];
    }
```

# 编辑距离
[题目连接：https://leetcode-cn.com/problems/edit-distance/](https://leetcode-cn.com/problems/edit-distance/)
核心思路：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210514171511962.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)

```cpp
class Solution {
    public int minDistance(String s1, String s2) {
        int n = s1.length();
        int m = s2.length();
        int[][] f = new int[n + 1][m + 1];
        for (int i = 0; i <= n; i++) f[i][0] = i;
        for (int j = 0; j <= m; j++) f[0][j] = j;
        for (int i = 1; i <= n; i++)
        {
            for (int j = 1; j <= m; j++)
            {
                f[i][j] = Math.min(f[i - 1][j] + 1, f[i][j - 1] + 1);
                if (s1.charAt(i - 1) == s2.charAt(j - 1)) f[i][j] = Math.min(f[i][j], f[i - 1][j - 1]);
                else f[i][j] = Math.min(f[i][j], f[i - 1][j - 1] + 1);
            } 
        }    
            return f[n][m];  
    }
}
    
```
# 变态跳台阶
[问题链接：https://www.nowcoder.com/practice/22243d016f6b47f2a6928b4313c85387?tpId=13&tags=&title=&difficulty=0&judgeStatus=0&rp=1](https://www.nowcoder.com/practice/22243d016f6b47f2a6928b4313c85387?tpId=13&tags=&title=&difficulty=0&judgeStatus=0&rp=1)
核心思路：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210526182346661.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)

```cpp
public class Solution {
    public int jumpFloorII(int target) {
        if(target < 2) {
            return 1;
        }
        int[] arr = new int[target + 1];
        arr[1] = 1;
        for(int i = 2; i <= target; i++) {
            arr[i] = 2 * arr[i - 1];
        }
        return arr[target];
    }
}
```
# 矩阵覆盖
**核心思路**
![](https://img-blog.csdnimg.cn/20210526233835998.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ1NjYxMTI1,size_16,color_FFFFFF,t_70)



**递归实现**

```cpp
public class Solution {
    public int rectCover(int target) {
        if(target < 1) {
            return 0;
        }else if(target <= 2) {
            return target;
        }else {
            return rectCover(target - 1) + rectCover(target - 2);
        }
    }
}
```
**迭代实现**

```cpp
public class Solution {
    public int rectCover(int target) {
        if(target < 1) {
            return 0;
        }else if(target <= 2) {
            return target;
        }
        int f1 = 1;
        int f2 = 2;
        int f3 = 0;
        for(int i = 3; i <= target; i++){
            //f3先更新
            f3 = f1 + f2;
            f1 = f2;
            f2 = f3;
            
            
        }
        return f3;
    }
}
```

**动态规划实现**

```cpp
public class Solution {
    public int rectCover(int target) {
        if(target < 1) {
            return 0;
        }else if(target <= 2) {
            return target;
        }
        int[] arr = new int[target + 1];
        arr[0] = 1;
        arr[1] = 1;
//         int ret = 0;
        for(int i = 2; i <= target; i++) {
            arr[i] = arr[i - 1] + arr[i - 2];
        }
        return arr[target];
    }
}
```
