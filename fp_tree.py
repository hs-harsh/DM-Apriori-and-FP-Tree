import collections
import itertools 
import timeit

def build_tree(itemsets, minsup):
    
    """ 
    Creates an FPTree for the given itemsets and minimum support.
    
    Parameters
    ----------
    itemsets : list of lists of strings
    minsup : int
        The minimum support threshold.

    Returns 
    -------
    tree : FPTree
    rank : dictionary
        Maps each item (string) to an int to define an ordering.
    """

    count = collections.defaultdict(int)
    for item in itertools.chain.from_iterable([itemset for itemset in itemsets]):
        count[item] += 1
    items = sorted([item for item in count if count[item] >= minsup], key=count.get)
    rank = {item:i for i,item in enumerate(items)}
    itemsets = [[item for item in itemset if item in rank] for itemset in itemsets]
#     print(itemsets)
    tree = FPTree(rank)
    for itemset in itemsets:
        itemset.sort(key=rank.get, reverse=True)
        tree.insert_itemset(itemset)
 
    return tree, rank

  
    
"""
    parameter : the text or the dat file to be loaded
    
    Returns all the itemsets (as a list of lists of strings) from a given file.

    The text file should have each itemset on one line with spaces between individual items, e.g.:
        1 20 13
        2 5 6 123
        1
        2 3
"""
def itemsets_from_file(filename):
    
    with open(filename, "r") as fin:
        itemsets = [[item for item in line.strip().split()] for line in fin]
    return itemsets

def frequent_itemsets(itemsets, minsup):
    
    """ Initiates the fpgrowth algorithm """
    tree = build_tree(itemsets, minsup)[0]
    for itemset in fpgrowth(tree, minsup):
        yield itemset
# itemsest are the frequent items which is to be shown in final answer
        
def fpgrowth(tree, minsup):
    
    """
    Performs the fpgrowth algorithm on the given tree to yield all frequent itemsets. 

    Parameters
    ----------
    tree : FPTree
    minsup : int

    Yields
    ------
    lists of strings
        Set of items that has occurred in minsup itemsets.
    """

    items = tree.nodes.keys()
    if tree.is_path:
        for i in range(1, len(items)+1):
            for itemset in itertools.combinations(items, i):
                yield tree.cond_items + list(itemset)
    else:
        for item in items:
            yield tree.cond_items + [item]
            cond_tree = tree.conditional_tree(item, minsup)
            for itemset in fpgrowth(cond_tree, minsup):
                yield itemset


class FPTree(object):
    def __init__(self, rank=None):
        self.root = FPNode(None)
        self.nodes = collections.defaultdict(list)
        self.cond_items = []
        self.rank = rank
    
    
    def conditional_tree(self, cond_item, minsup):
        """ 
        Creates and returns the subtree of self conditioned on cond_item.
        
        Parameters
        ----------
        cond_item : int | str
            Item that the tree (self) will be conditioned on.
        minsup : int 
            Minimum support threshold.

        Returns
        -------
        cond_tree : FPtree
        """
        # Find all path from root node to nodes for item
        branches = []
        count = collections.defaultdict(int)
        for node in self.nodes[cond_item]:
            branch = node.itempath_from_root()
            branches.append(branch)
            for item in branch:
                count[item] += node.count

        # Define new ordering, otherwise deep trees may have combinatorially explosion
        items = [item for item in count if count[item]>=minsup]
        items.sort(key=count.get)
        rank = {item:i for i,item in enumerate(items)}
        
        # Create conditional tree
        cond_tree = FPTree(rank)
        for i,branch in enumerate(branches):
            branch = sorted([item for item in branch if item in rank], key=rank.get, reverse=True)
            cond_tree.insert_itemset(branch, self.nodes[cond_item][i].count)
        cond_tree.cond_items = self.cond_items + [cond_item]
        
        return cond_tree

    
    def insert_itemset(self, itemset, count=1):
        """ 
        Inserts a list of items into the tree.
        
        Parameters
        ----------
        itemset : list 
            Items that will be inserted into the tree.
        count : int
            The number of occurrences of the itemset.
        """
        if len(itemset) == 0:
            return
        
        # Follow existing path in tree as long as possible
        index = 0
        node = self.root
        for item in itemset:
            if item in node.children:
                child = node.children[item]
                child.count += count
                node = child
                index += 1
            else:
                break
        
        # Insert any remaining items
        for item in itemset[index:]:
            child_node = FPNode(item, count, node)
            self.nodes[item].append(child_node)
            node = child_node
    

    @property
    def is_path(self):
        if len(self.root.children) > 1:
            return False
        for i in self.nodes:
            if len(self.nodes[i])>1 or len(self.nodes[i][0].children)>1:
                return False
        return True

class FPNode(object):
    def __init__(self, item, count=1, parent=None):
        self.item = item    
        self.count = count
        self.parent = parent
        self.children = collections.defaultdict(FPNode)
        
        if parent != None:
            parent.children[item] = self


    def itempath_from_root(self):
        """ Returns the top-down sequence of items from self to (but not including) the root node. """
        path = []
        if self.item == None:
            return path
        
        node = self.parent
        while node.item != None:
            path.append(node.item)
            node = node.parent
        
        path.reverse()
        return path


# to calculate total time to run the code start time is taken from here
start_time = timeit.default_timer()

#take input from file using the function itemsets_from_file
itemsets = itemsets_from_file("/content/drive/My Drive/Colab Notebooks/DM Assignment/forests.txt")                 
#minsup is the minimum support required          
minsup = 0.89
l=len(itemsets)
print(l)
# frequent_itemsets function initiates the fptree generation
fis = [itemset for itemset in frequent_itemsets(itemsets, int(minsup)*l)]
fis.sort(key=len)
print ("Frequent Itemset are")
# for items in fis:
#     print (items)
print(fis)
    
elapsed = timeit.default_timer() - start_time
print("Time taken: ")
print(elapsed)

import pandas as pd,timeit
col = ['Dataset','Minsup', 'Minsup_count', 'Time taken', 'Size of Frequent Set']
result = pd.DataFrame(columns=col)

count=0
#take input from file using the function itemsets_from_file
itemsets = itemsets_from_file("/content/drive/My Drive/Colab Notebooks/DM Assignment/forests.txt") 
l=len(itemsets)
minsup=0.48
factor=(0.02)
print(l)
while(minsup<0.92):
  count+=1
  print(count)
  minsup+=factor
  start_time = timeit.default_timer()
  # frequent_itemsets function initiates the fptree generation
  supcount=int(l*minsup)
  fis = [itemset for itemset in frequent_itemsets(itemsets, supcount)]
#     fis = [itemset for itemset in frequent_itemsets(itemsets, supcount)]
  fis.sort(key=len)
  if(len(fis)==0):
    break
  elapsed = timeit.default_timer() - start_time
  output=["Forest Dataset"]
  output.append(minsup)
  output.append(supcount)
  output.append(elapsed)
  output.append(len(fis))
  df2 = pd.DataFrame([output],columns=col)
  result=pd.concat([result,df2],ignore_index=True)
print(result)
print(count)
file_name="/content/drive/My Drive/Colab Notebooks/DM Assignment/forests_analysis.csv"
result.to_csv(file_name, sep='\t')

import pandas as pd
col = ['Dataset','Minsup', 'Minsup_count', 'Time taken', 'Size of Frequent Set']
result = pd.DataFrame(columns=col)
# s1 = pd.Series([5, 6, 7,8,9])


count=0
#take input from file using the function itemsets_from_file
itemsets = itemsets_from_file("/content/drive/My Drive/Colab Notebooks/DM Assignment/bog.txt") 
l=len(itemsets)
minsup=0.2
factor=(0.02)

while(minsup<0.64):
  count+=1
  print(count)
  minsup+=factor
  start_time = timeit.default_timer()
  # frequent_itemsets function initiates the fptree generation
  supcount=int(l*minsup)
#     fis = [itemset for itemset in maximal_frequent_itemsets(itemsets, int(minsup)*l)]
  fis = [itemset for itemset in frequent_itemsets(itemsets, supcount)]
  fis.sort(key=len)
  if(len(fis)==0):
    break
  elapsed = timeit.default_timer() - start_time
#     print("Time taken: ")
#     print(elapsed)
  output=["Bog Dataset"]
  output.append(minsup)
  output.append(supcount) 
  output.append(elapsed)
  output.append(len(fis))
  df2 = pd.DataFrame([output],columns=col)
  result=pd.concat([result,df2],ignore_index=True)
print(result)
print(count)
file_name="/content/drive/My Drive/Colab Notebooks/DM Assignment/bog_analysis.csv"
result.to_csv(file_name, sep='\t')

