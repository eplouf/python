#!/usr/bin/env python3

# retrieved the csv from https://www.insee.fr/fr/information/4769950 ,
# beware, the years are overlaping, some deaths are reported months after
# they occured in some case, so you have to run the process on multiple
# files, like:
#  /insee_deces$ ./insee_deaths_by_months.py "2020 2019 2018 2017 2016 2015 2014 2013 2012 2011 2010 2009 2008" deces-2020-m01.csv Deces_2020_M0*.csv deces-2019.csv deces-2018.csv deces-2017.csv deces-2016.csv deces-2015.csv deces-2014.csv deces-2013.csv deces-2012.csv deces-2011.csv deces-2010.csv deces-2009.csv deces-2008.csv
#          2020    2019    2018    2017    2016    2015    2014    2013    2012    2011    2010    2009    2008
#  12              55610   53732   57792   58132   51409   53159   51116   52066   50500   51158   49854   50930
#  11              52577   50432   50813   50506   47317   47596   45960   47326   45779   45353   44729   44214
#  10              51040   50667   50253   51114   50739   47160   46715   47773   46676   47282   46400   45756
#  09      40055   46812   46489   46923   45503   45294   44224   43573   42898   41533   42974   41512   41603
#  08      49171   47719   48035   47434   46556   46533   44921   43285   43865   43122   42868   42705   42150
#  07      47407   48819   49053   47144   47480   47153   45346   45893   44622   43114   44036   42868   43478
#  06      46602   47073   45698   45176   45050   45241   43874   43733   43306   42562   43444   42408   42190
#  05      49526   49745   48555   49114   48722   46860   46188   45986   46513   44494   45833   44274   44468
#  04      67406   49789   51119   47684   49423   48370   46083   47546   47393   44017   45361   44923   46061
#  03      63627   54388   61203   50961   54905   55702   49951   54818   54436   47833   49123   47826   48467
#  02      51882   56509   52908   53295   50082   58110   47290   52154   55181   46268   47335   48050   47317
#  01      57952   61200   60623   68969   54824   59196   51830   56851   53051   53126   52874   60586   53478

import sys

yearmont = []
sums = {}
months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
months.reverse()


def csv_get(csv=None):
    fields = csv.split('";"')
    for field in fields:
        field.strip()
    return fields


def feed(csvfile):
    with open(csvfile, "r") as f:
        # this is header
        f.readline()
        yearmont = []
        while True:
            fields = csv_get(csv=f.readline())
            # as date is in the sixth field
            try:
                date = fields[6]
                date_year = date[:4]
                date_yearmonth = date[:6]
                if date_yearmonth != "":
                    yearmont.append({
                        "date": date_year,
                        "sex": fields[1],
                        "death": date_yearmonth
                    })
            except IndexError:
                break
    return yearmont


def sumsum(data):
    for who in data:
        sums[who['death']] = sums.get(who['death'], 0) + 1


# =====

if len(sys.argv) < 3:
    print("""Usage: %s [raw|table] <"years list"> <filelist.csv ..>""" % sys.argv[0])
    sys.exit(-1)
showmode = "table"
idxarg = 2
if sys.argv[1] == "raw":
    showmode = "raw"
    idxarg = 3

# =====

for csvfile in sys.argv[idxarg:]:
    yearmont.append(feed(csvfile))

for data in yearmont:
    try:
        data.sort(key=lambda x: int(x['death']))
    except ValueError:
        print(sys.exc_info())
    sumsum(data)


# =====

if showmode == "raw":
    for count in sums:
        print(f"{count} {sums[count]}")
else:
    years = sys.argv[1].split()

    for year in years:
        print(f"\t{year}", end='')
    print()
    for month in months:
        print(f"{month}\t", end='')
        for year in years:
            yearmonth = "%s%s" % (year, month)
            try:
                print(f"{sums[yearmonth]}\t", end='')
            except KeyError:
                # ok, seems fair
                print("\t", end='')
        print()
