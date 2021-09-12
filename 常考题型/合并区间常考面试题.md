@[TOC](合并区间)
# 合并区间
[https://www.nowcoder.com/practice/69f4e5b7ad284a478777cb2a17fb5e6a?tpId=117&&tqId=37737&&companyId=665&rp=1&ru=/company/home/code/665&qru=/ta/job-code-high/question-ranking](https://www.nowcoder.com/practice/69f4e5b7ad284a478777cb2a17fb5e6a?tpId=117&&tqId=37737&&companyId=665&rp=1&ru=/company/home/code/665&qru=/ta/job-code-high/question-ranking)
```java
public class Solution {
    public ArrayList<Interval> merge(ArrayList<Interval> intervals) {
        ArrayList<Interval> ret = new ArrayList<>();
        if(intervals == null || intervals.size() == 0) {
            return ret;
        }
        intervals.sort((a, b)->(a.start - b.start));
        ret.add(intervals.get(0));
        for(int i = 1; i < intervals.size(); i++) {
            int left = intervals.get(i).start;
            int right = intervals.get(i).end;
            if(ret.get(ret.size() - 1).end < left) {
                ret.add(new Interval(left, right));
            }else {
                ret.get(ret.size() - 1).end = Math.max(ret.get(ret.size() - 1).end, right);
            }
        }
        return ret;
    }
}
```
# 合并区间
[https://leetcode-cn.com/problems/merge-intervals/](https://leetcode-cn.com/problems/merge-intervals/)
```java
class Solution {
    public int[][] merge(int[][] intervals) {
        Arrays.sort(intervals, (a,b)->a[0] - b[0]);
        int[][] ret = new int[intervals.length][2];
        int index = -1;
        for(int[] nums : intervals) {
            if(index == -1 || nums[0] > ret[index][1]) {
                ret[++index] = nums;
            }else {
                ret[index][1] = Math.max(ret[index][1], nums[1]);
            }
        }
        return Arrays.copyOf(ret, index + 1);
    }
}
```

