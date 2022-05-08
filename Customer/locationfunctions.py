from Agents.models import AgentLocation, AgentShopCategorie, AgentsUsers, AgentProducts
from . import models
from math import sin, cos, sqrt, atan2, radians
from NapsackAdmin.models import ShopsCategories

def find_distance(flat, flong, llat, llong):

    R = 6373.0

    lat1 = radians(float(flat))
    lon1 = radians(float(flong))

    lat2 = radians(float(llat))
    lon2 = radians(float(llong))

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance


# Python program for implementation of MergeSort

# Merges two subarrays of arr[].
# First subarray is arr[l..m]
# Second subarray is arr[m+1..r]


def merge(arr, l, m, r):
    n1 = m - l + 1
    n2 = r - m

    # create temp arrays
    L = [0] * (n1)
    R = [0] * (n2)
    Lun = [0] * (n1)
    Run = [0] * (n2)
    Llat = [0] * (n1)
    Rlat = [0] * (n2)
    Llong = [0] * (n1)
    Rlong = [0] * (n2)

    # Copy data to temp arrays L[] and R[]
    for i in range(0, n1):
        temp_dis = arr[l + i]
        L[i] = temp_dis['distance']
        Lun[i] = temp_dis['username_id']
        Llat[i] = temp_dis['latitude']
        Llong[i] = temp_dis['longitude']


    for j in range(0, n2):
        temp_dis = arr[m + 1 + j]
        R[j] = temp_dis['distance']
        Run[j] = temp_dis['username_id']
        Rlat[j] = temp_dis['latitude']
        Rlong[j] = temp_dis['longitude']

    # Merge the temp arrays back into arr[l..r]
    i = 0	 # Initial index of first subarray
    j = 0	 # Initial index of second subarray
    k = l	 # Initial index of merged subarray

    while i < n1 and j < n2:
        if L[i] <= R[j]:
            temp_dis = arr[k]
            temp_dis['distance'] = L[i]
            temp_dis['username_id'] = Lun[i]
            temp_dis['latitude'] = Llat[i]
            temp_dis['longitude'] = Llong[i]
            i += 1
        else:
            temp_dis = arr[k]
            temp_dis['distance'] = R[j]
            temp_dis['username_id'] = Run[j]
            temp_dis['latitude'] = Rlat[j]
            temp_dis['longitude'] = Rlong[j]
            j += 1
        k += 1

    # Copy the remaining elements of L[], if there
    # are any
    while i < n1:
        temp_dis = arr[k]
        temp_dis['distance'] = L[i]
        temp_dis['username_id'] = Lun[i]
        temp_dis['latitude'] = Llat[i]
        temp_dis['longitude'] = Llong[i]
        i += 1
        k += 1

    # Copy the remaining elements of R[], if there
    # are any
    while j < n2:
        temp_dis = arr[k]
        temp_dis['distance'] = R[j]
        temp_dis['username_id'] = Run[j]
        temp_dis['latitude'] = Rlat[j]
        temp_dis['longitude'] = Rlong[j]
        j += 1
        k += 1

# l is for left index and r is right index of the
# sub-array of arr to be sorted


def mergeSort(arr, l, r):
    if l < r:

        # Same as (l+r)//2, but avoids overflow for
        # large l and h
        m = l+(r-l)//2

        # Sort first and second halves
        mergeSort(arr, l, m)
        mergeSort(arr, m+1, r)
        merge(arr, l, m, r)


# # Driver code to test above
# arr = [12, 11, 13, 5, 6, 7]
# n = len(arr)
# print("Given array is")
# for i in range(n):
#     print("%d" % arr[i],end=" ")
#
# mergeSort(arr, 0, n-1)
# print("\n\nSorted array is")
# for i in range(n):
#     print("%d" % arr[i],end=" ")
#
# # This code is contributed by Mohit Kumra


def shopinfo(locinfo):
    locshops = AgentShopCategorie.objects.all().values()
    temp_info = []
    for alls in locshops:
        for loc in locinfo:
            find = AgentProducts.objects.filter(agentsusers=loc['username_id']).values()
            if alls['username_id'] == loc['username_id'] and find:
                temp = alls
                temp_scat = ShopsCategories.objects.filter(Shops_id=alls['agent_shop_categorie_id']).values()
                temp_shopname = AgentsUsers.objects.filter(agen_user_id=alls['username_id']).values()
                img_url = AgentsUsers.objects.get(agen_user_id=alls['username_id'])
                temp_sanem_one = temp_scat[0]
                temp_shopname_one = temp_shopname[0]
                temp['distance'] = loc['distance']
                temp['name'] = temp_sanem_one['name']
                temp['agent_shop_name'] = temp_shopname_one['agent_shop_name']
                temp['agent_id'] = temp_shopname_one['agen_user_id']
                temp['img'] = img_url
                temp_info.append(temp)
    return temp_info


def shoploc(lat, long):
    print(lat)
    agents_loc = AgentLocation.objects.all().values()
    # print(agents_loc)
    temp_agents_loc = agents_loc
    for aloc in temp_agents_loc:
        aloc['distance'] = find_distance(lat,long,aloc['latitude'],aloc['longitude'])
    for i in temp_agents_loc:
        print(i)
    temp_agents_dis = []
    for adis in temp_agents_loc:
        if adis['distance'] <= 25:
            temp_agents_dis.append(adis)

    n = len(temp_agents_dis)
    print(n)
    mergeSort(temp_agents_dis, 0, n - 1)
    print("ttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt")
    for i in temp_agents_dis:
        print(i)
    final = shopinfo(temp_agents_dis)
    print(len(final))
    print(final)
    return final



















# insert the data

# m = models.Members(firstname="adil", lastname="k")
# m.save()
# print(m)
# k or kumar


# geting all fileds with the list of dist

# m = models.Members.objects.all().values()
# print(m)
# {'id': 1, 'firstname': 'nanda', 'lastname': 'k'}, {'id': 2, 'firstname': 'kumar', 'lastname': 'k'},]


# to delete the rows

# member = models.Members.objects.get(id=1)
# member.delete()
# print(models.Members.objects.all().values())


# to update the recodes

# member = models.Members.objects.get(id=2)
# member.firstname = "first"
# member.lastname = "last"
# member.save()
# print(models.Members.objects.all().values())


# to get all list of objects

# mydata = models.Members.objects.all()
# print(mydata)
#
# list of objects <QuerySet [<Members: last>, <Members: k>]>


# to get list of all values in the form of dist

# mydata = models.Members.objects.all().values()


# to get one column values


# mydata = models.Members.objects.values_list('firstname').values()
# print(mydata)
# list with tuples <QuerySet [('first',), ('adil',)]>


# to get specific row

# mydata = models.Members.objects.filter(firstname='adil').values()
# mydata = models.Members.objects.filter(lastname='Refsnes', id=2).values()
# mydata = Members.objects.filter(firstname='Emil').values() | Members.objects.filter(firstname='Tobias').values()
# .filter(firstname__startswith='L');
# out will be list with dist


# order by
# ass mydata = Members.objects.all().order_by('firstname').values()
# dess mydata = Members.objects.all().order_by('-firstname').values()
# Multiple Order Bys
# mydata = Members.objects.all().order_by('lastname', '-id').values()

# all_category = models.ProductsCategories.objects.filter(shop_id="0210204445e14f4395a6042a914641e9").order_by('name').values()
# print(all_category)

# all_category = models.Products.objects.filter(categories_id="4987137b-8f52-44f4-b59f-368846c65133")
# print(all_category)

# return HttpResponse("<h1>welcome</h1>")

