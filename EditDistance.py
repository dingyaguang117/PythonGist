#coding=utf-8
'''
Author:Yaguang Ding
Mail:dingyaguang117@gmail.com
Date:2012/6/4
'''

class EditDistance():
    def __init__(self):
        pass
    
    def mymin(self,L):
        min = L[0]
        for item in L:
            if item < min:min=item
        return min
    
    def EditDistance(self,s1,s2):
        if type(s1) != unicode or type(s2)!= unicode:
            raise Exception('EditDistance:s1,s2 should be unicode')
        len1 = len(s1)
        len2 = len(s2)
        dp = [[0]*(len2+1) for i in range(len1+1)]
        for i in range(0,len1+1): dp[i][0] = i
        for i in range(0,len2+1): dp[0][i] = i
        for i in range(1,len1+1):
            for j in range(1,len2+1):
                n1 = dp[i-1][j-1]
                n2 = dp[i-1][j] + 1
                n3 = dp[i][j-1] + 1
                if s1[i-1] != s2[j-1]:n1 += 1
                dp[i][j] = self.mymin([n1,n2,n3])
        return dp[len1][len2]
    
    
    def Similarity(self,s1,s2):
        d = self.EditDistance(s1, s2)
        len1 = len(s1)
        len2 = len(s2)
        sim = 1-1.0*(d-abs(len1-len2))/self.mymin([len1,len2])
        sim *= self.mymin([len1,len2])*1.0/(len1+len2-self.mymin([len1,len2]))
        return sim


if __name__ == '__main__':
    _EditDistance = EditDistance()
    
    print _EditDistance.Similarity(u'a',u'b')
    print _EditDistance.Similarity(u'ad',u'adbc')
    print _EditDistance.Similarity(u'abcde',u'bcde')
    print _EditDistance.Similarity(u'中国',u'中华人民共和国')
    
