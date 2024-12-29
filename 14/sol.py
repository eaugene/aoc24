from utils import timeit

FILE = "inp.txt"
def read():
    values = []
    with open(FILE) as f:
        for line in f:
            # Split the string into p and v parts
            parts = line.split(" ")

            # Extract the p values and convert them to a tuple of integers
            p = tuple(map(int, parts[0][2:].split(",")))

            # Extract the v values and convert them to a tuple of integers
            v = tuple(map(int, parts[1][2:].split(",")))

            # Append both p and v as a list to the values list
            values.append([p[0],p[1] ,v[0],v[1]])
    return values


@timeit
def solve1(val):
    n = 7
    m = 11
    if FILE == "inp.txt":
        n = 103
        m = 101

    grid  = [[0 for i in range(m)] for j in range(n)]
    for v in val:
        px,py,vx,vy = v
        vx = (vx + m) % m
        vy = (vy + n) % n

        px = (px + (vx*100))%m
        py = (py + (vy*100))%n

        grid[py][px] += 1

    # for i in range(n):
    #     for j in range(m):
    #        print(grid[i][j],end=" ")
    #     print("")

    quads = [[0,0,n//2,m//2],[0,m//2+(m%2),n//2,m],[n//2+(n%2),m//2+(m%2),n,m],[n//2+(n%2),0,n,m//2]]

    ans = 1
    for q in quads:
        x1,y1,x2,y2 = q
        count = 0
        for i in range(x1,x2):
            for j in range(y1,y2):
                count += grid[i][j]
        ans *= count

    return ans


@timeit
def solve2(val):
    n = 7
    m = 11
    if FILE == "inp.txt":
        n = 103
        m = 101

    def getLCM():
        """
        GCD * LCM = a*b
        LCM = (a*b)/GCD
        :return:
        """

        """
        as both n , m are prime here the gcd is going to be 1 
        """
        return n*m

    repeatPoint = getLCM()

    # handle the negative velocities
    for i in range(len(val)) :
        px,py,vx,vy = val[i]
        vx = ( vx + m ) % m
        vy = ( vy + n ) % n
        val[i] = [px,py,vx,vy]

    def getGridAfterTime(t):
        grid = [[0 for i in range(m)] for j in range(n)]
        for v in val:
            px,py,vx,vy = v
            px = (px + (vx*t) )%m
            py = (py + (vy*t) )%n
            grid[py][px] += 1
        return grid

    def getDenseOfGrid(grid):

        vis = [[False for x in range(m)] for y in range(n)]

        def isLimit(x,y):
            return 0 <= x < n and 0 <= y < m

        def dfs(x,y):
            if not isLimit(x,y) or vis[x][y] or grid[x][y] == 0:
                return 0
            vis[x][y] = True
            return 1 + dfs(x+1,y) + dfs(x-1,y) + dfs(x,y+1) + dfs(x,y-1)

        ans = 0
        for i in range(n):
            for j in range(m):
                if not vis[i][j] and grid[i][j] > 0:
                    ans = max(ans,dfs(i,j))
        return ans

    denseList = []
    for i in range(repeatPoint):
        grid = getGridAfterTime(i)
        denseList.append((getDenseOfGrid(grid),i))


    denseList.sort(key=lambda x: (-x[0], x[1]))
    """
    The idea behind here is to find the time at which the grid is most dense
    Suspecting the dense would from the christmas tree shape ( clue : Reddit )  
    FYI - the question was very vague . Christmas tree can be hollow as well ( fail case ) and the dense can be any shape ( another fail case )  
    
    """
    grid = getGridAfterTime(denseList[0][1])
    for i in range(n):
        for j in range(m):
            if grid[i][j] > 0:
                print("*",end="")
            else:
                print(" ",end="")
        print("")
    return denseList[0][1]

val = read()
print(solve1(val))
print(solve2(val))

"""
Function 'solve1' executed in 0.0006 seconds
229839456
   *                                                                                                 
          *                                                                      *     *             
                                                                                                     
                                                                                                     
                                                                                                     
                *                                  *                                *                
                                                      *                                              
               *                                                                                     
                                                                                                     
                                         *                                     *                     
                    *                              *                                                 
                                                   *                                     *   *       
                                                                *                                    
                                                          *                                          
                                                                                        *        *   
                                                                                                     
                                                                                                     
                                                                                                     
        *                                         *                                                  
                                     *                    *                                          
                                   *                                                         *       
                  *                                                                                  
                                           *                                                         
                                                    * **                       *               *     
                                          *                                                          
* *                    *  *  *                          *                                            
         *                                      *                                      *             
                                                                   *                                 
                         *  *******************************               *               *          
                            *                             *   *                                      
                            *                             *                                          
                            *                             *       *             *                    
                      *     *                             *                     *                    
                            *              *              *      *                    *              
                            *             ***             *                                          
 *                          *            *****            *                              *           
                            *           *******           *               *                          
                            *          *********          *                                          
                            *            *****            *                                   *      
                            *           *******           *                                          
             *              *          *********          *                                          
                            *         ***********         *   *                                      
                            *        *************        *                                         *
                            *          *********          *                                          
                            *         ***********         * *                                        
                            *        *************        *                         *                
                            *       ***************       *                                          
                     *      *      *****************      *                                          
                            *        *************        *                                          
                            *       ***************       *      *                                   
                        *   *      *****************      *                            *             
      *         *           *     *******************     *          *               *               
                            *    *********************    *                                          
                            *             ***             *                                          
                            *             ***             *                                   *      
                            *             ***             *                                    *    *
                            *                             *                      *                   
 *                          *                             *  *                                       
                            *                             *                                          
        *                   *                             *       *                                  
                            *******************************                  *    *                  
                                                                             *                       
                                                                                                     
                                                            *            *                           
                                                                                                     
                                                              *                                      
            *                  *                                                                     
                                                                                                     
                       *                                                                             
                                                  *              *                                   
                                                   *                                *            *   
                                                               *                                     
                          *                                                *                         
   *                        *                                                                   *    
                                                                            *                        
           *   *               *                  *                               *                  
                                                                                         *           
                         *                                                                           
                                                            *                 *                      
                                                                              *      *               
                                             *                                                       
                                            *                     *                                  
                                                                      *   *                          
        *                                                 *                                          
                                *           *                                                     *  
                                                                                        *            
      *                   *                                                                          
                                                            *                                        
                                 *                                                                   
                                                                             *                       
                                                                                             *       
                 *                                                                                   
                                                                                                     
                                  *                                                     *            
                                                                                                     
   *          *                     *                                                                
              *                                                                                      
        *                                                                *                           
                                                                                           *         
                     *                             *                *                  *      *      
                  *                                                                                  
                                        *                                              *             
            *                                                                                        
Function 'solve2' executed in 14.5912 seconds
7138
"""



