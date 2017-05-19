import scrapy
import os
import re

base_url = 'http://neuromorpho.org/neuron_info.jsp?neuron_name='
neuron_folder = 'neurons/'
output_folder = 'output/'

class LFeatureSpider(scrapy.Spider):
    name = "l-feature"
    urls = []
    filepaths = []

    def read_in_all_neurons(self):
        dirs = os.listdir(neuron_folder)
        for dir in dirs:
            files = os.listdir(neuron_folder + dir)
            for file in files:
                self.urls.append(base_url + file.split(".")[0])
                self.filepaths.append(output_folder + dir + '/' + file.split('.')[0] + '.txt')

    def start_requests(self):
        self.read_in_all_neurons()
        for url, filepath in zip(self.urls, self.filepaths):
            yield scrapy.Request(url=url, callback=self.parse, meta={'pos' : filepath})

    def parse(self, response):
        # name = response.url.split("=")[-1]
        filename = response.meta['pos'];
        info = response.css('table[id=NeuronInfotable11]')
        itemnames = info.css('td[align=right]::text').extract()
        itemvalues = info.css('td[align=left]::text').extract()

        itemnames[:] = [re.sub('[^a-zA-z0-9\.]', '', itemname) for itemname in itemnames]
        itemvalues[:] = [re.sub('[^0-9\.]', '', itemvalue) for itemvalue in itemvalues]

        # print(filename)
        # print(itemnames)
        # print(itemvalues)
        dir_path = filename[:filename.rfind('/')]
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

        with open(filename, 'w') as f:
            for itemname, itemvalue in zip(itemnames[2:], itemvalues[2:]):
                f.write(itemname + " " + itemvalue + '\n')
        self.log('Saved file %s' % filename)