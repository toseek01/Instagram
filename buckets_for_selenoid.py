class bloggerDistribution:
    
    def __init__(self,data,target_buckets):
        '''Parameters:
        - data : dataframe with blogger name and followers count
        Exmp: 
        data.head()
            blogger   | followers_count
            her.perdol| 95 305
            don.gandon| 321 045
                    .
                    .
                    .
            dura_ventura | 117411
            
        - buckets: number drivers we have
        '''
        
        self.data = data
        self.target_bloggers = data.shape[0]
        self.target_buckets = target_buckets
        self.bestDistr = 0
        self.bestStd = 0
        
    def bornFunction(self):
        
        idx = np.random.randint(0,self.target_buckets,self.target_bloggers)
        
        return idx
    
    def throwBuckets(self,distribution):
        
        Buckets = np.zeros(self.target_buckets)
        
        for bucket_num in range(self.target_buckets):
            
            Buckets[bucket_num] = self.data.followers_count.values[np.where(distribution == bucket_num)].sum()
        
        return Buckets
    
    def costFunction(self,Buckets):
        
        Cost = np.std(Buckets)
        
        return Cost
        
        
    def coordinator(self,iters):
        '''
        iters - number iterations
        '''
        
        distribution = self.bornFunction()
        
        Buckets = self.throwBuckets(distribution)
        
        Cost = self.costFunction(Buckets)
        
        self.bestDistr = distribution
        self.bestStd = Cost
        
        print("Initial STD : %i"% (self.bestStd),file =sys.stderr,flush = True)
        
        for i in range(iters):
            
            distribution = self.bornFunction()
            Buckets = self.throwBuckets(distribution)
            Cost = self.costFunction(Buckets)
            
            if Cost < self.bestStd:
                
                self.bestDistr = distribution
                self.bestStd = Cost
                print("Current STD : %i"% (Cost),file =sys.stderr,flush = True,end='\r')
            
            else:
                pass
if __name__=='__main__':
    
    iOpt = bloggerDistribution(df,3)
    iOpt.coordinator(1000000)
    iOpt.bestDistr