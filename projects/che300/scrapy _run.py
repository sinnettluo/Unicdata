import pp
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def crawlrun(part,parts):
    process = scrapy.crawler.CrawlerProcess(scrapy.utils.project.get_project_settings())
    # 'followall' is the name of one of the spiders of the project.
    process.crawl('che300_price',part=part,parts=parts)
    process.start() # the script will block here until the crawling is finished

def ppexcut(parts):
    ppservers = ()
    job_server = pp.Server(parts,ppservers=ppservers)
    print "Starting pp with", job_server.get_ncpus(), "workers"
    jobs=[]
    for index in xrange(parts):
        #print index
        # Submit a job which will test if a number in the range starti-endi has given md5 hash
        # parse - the function
        # (starti, step) - tuple with arguments for md5test
        # () - tuple with functions on which function md5test depends
        # ("md5",) - tuple with module names which must be imported before md5test execution
        jobs.append(job_server.submit(func=crawlrun, args=(index, parts),
                               depfuncs=(),
                               modules=("pp","scrapy","scrapy.crawler","scrapy.utils.project")))
    # Retrieve results of all submited jobs
    for job in jobs:
          result = job()
    # wait for jobs in all groups to finish
    #job_server.wait()
    job_server.print_stats()
#crawlrun(0,8)
ppexcut(6)