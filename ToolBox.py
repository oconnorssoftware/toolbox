import json

def dictdif(dicfrm,dicto):
  ddict={}
  frmkv=dicfrm.keys()
  tokv=dicto.keys()
  #frmiv=dicfrm.viewitems()
  #toiv=dicto.viewitems()
  ddict["Ratr"]=[x for x in frmkv-tokv]#'-'+
  #ddict["atr"].extend(['+'+x for x in tokv-frmkv])
  ddict["vals"]=[[k,v] for k,v in dicto.items() if(k not in dicfrm or dicfrm[k]!=v)]
  #ddict["vals"]=[x for x in toiv-frmiv]
  return ddict

def treeify(nodeList = [],parent = ""):
  '''
    takes list of nodes (dictionaries) of a tree and turns them into
    a JSONish tree.
    nodeList = [
      {#branch
        "Parent":"",
        "BranchID":"abc123",
        "BranchName":"This is the root node"
      },
      {#leaf
        "LeafName":SomeUser,
        "BranchID":"abc123",
        "_id":"someUserID"
      },
      {#branch
        "Parent":"abc123",
        "BranchID":"abc124",
        "BranchName":"This is the sub node"      
      },
      {#leaf
        "LeafName":SomeOtherUser,
        "BranchID":"abc124",
        "_id":"someUserID2"
      },
    ]
  '''
  #listOfparents
  tmpList = []
  for node in nodeList:
    if "Parent" in node:#then this is a group
      if node['Parent'] == parent:
        #this removes the branch we are about to add and walk from being checked again.
        #we do the 'or "UserName" in x' because we want the leaf nodes to not get kicked out.
        newnodeList = [x for x in nodeList if x["BranchID"] != node['BranchID'] or "LeafName" in x]
        tmpList.append({
            "text":node["BranchName"],
            "userID":node['BranchID'],
            "group":True,
            "leaf":False,
            "children":treeify(newnodeList,node["BranchID"])
          })
    elif "LeafName" in node:#then this is a user (leaf)   
      if node['BranchID'] == parent:
        tmpList.append({
            "text":node["LeafName"],
            "userID":node["_id"],
            "leaf":True,
            "group":False
          })
  return tmpList

if __name__ == '__main__':
  nodeList = [
      {#branch
        "Parent":"",
        "BranchID":"abc123",
        "BranchName":"This is the root node"
      },
      {#leaf
        "LeafName":"SomeUser",
        "BranchID":"abc123",
        "_id":"someUserID"
      },
      {#branch
        "Parent":"abc123",
        "BranchID":"abc124",
        "BranchName":"This is the sub node"      
      },
      {#leaf
        "LeafName":"SomeOtherUser",
        "BranchID":"abc124",
        "_id":"someUserID2"
      },
    ]
  print(treeify(nodeList))

  