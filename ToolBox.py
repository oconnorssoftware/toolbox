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

def findChildren(TopLevelGroupID = "",GroupID = "", nodes = []):#finds subgroups
  nodes = nodes or []
  if GroupExists(TopLevelGroupID,GroupID):
    children = Objects.GROUP_COLLECTIONS[TopLevelGroupID].find({"Parent":GroupID})
    for child in children:
      nodes.append(child)
      findChildren(TopLevelGroupID=TopLevelGroupID, GroupID=child['_id'], nodes=nodes)
    return nodes
  else:
    LOGGER.error("findChildren failed - TopLevelGroup:{} or SubGroup:{} does not exist".format(TopLevelGroupID,GroupID))
    return False

def findLeaves(TopLevelGroupID,GroupIDs):
  retList = []
  for GroupID in GroupIDs:
    if not GroupExists(TopLevelGroupID,GroupID):
      LOGGER.error("findLeaves failed - TopLevelGroup:{} or SubGroup:{} does not exist".format(TopLevelGroupID,GroupID))
      return False
    retList += list(Objects.NEW_USER_COLLECTION[TopLevelGroupID].find({"GroupID":GroupID}))
  return retList

def GetTree(TopLevelGroupID = "", GroupID = ""):
  try:
    if not TopLevelGroupExists(TopLevelGroupID):
      LOGGER.error("UserAPI.GetFullTree({}) - failed due to TopLevelGroup not existing".format(TopLevelGroupID))
      return False
    parent = Objects.GROUP_COLLECTIONS[TopLevelGroupID].find_one({'_id':GroupID})
    branches = findChildren(TopLevelGroupID = TopLevelGroupID, GroupID = GroupID)
    branches.append(parent)
    GroupIDsToFetchUsersFor = [x['_id'] for x in branches]
    leaves = findLeaves(TopLevelGroupID,GroupIDsToFetchUsersFor)
    leavesAndBranches = branches + leaves
    tree = treeify(nodeList = leavesAndBranches, parent = None)
    return tree
  except:
    LOGGER.error("UserAPI.GetFullTree({}) - failed".format(TopLevelGroupID))
    return False

def treeify(nodeList = [],parent = ""):

  #listOfparents
  tmpList = []
  for node in nodeList:
    if "Parent" in node:#then this is a group
      if node['Parent'] == parent:
        #this removes the branch we are about to add and walk from being checked again.
        #we do the 'or "UserName" in x' because we want the leaf nodes to not get kicked out.
        newnodeList = [x for x in nodeList if x["GroupID"] != node['GroupID'] or "UserName" in x]
        tmpList.append({
            "text":node["GroupName"],
            "userID":node['GroupID'],
            "group":True,
            "leaf":False,
            "children":treeify(newnodeList,node["GroupID"])
          })
    elif "UserName" in node:#then this is a user (leaf)   
      if node['GroupID'] == parent:
        tmpList.append({
            "text":node["UserName"],
            "userID":node["_id"],
            "leaf":True,
            "group":False
          })
  return tmpList