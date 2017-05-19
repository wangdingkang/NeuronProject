import scrapy
import os

base_url = 'http://neuromorpho.org/neuron_info.jsp?neuron_name='
neuron_folder = 'neurons/'

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
                self.filepaths.append(neuron_folder + dir + '\\' + file.split('.')[0] + '.txt')

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

        itemnames[:] = [itemname.split(u'\xa0')[0].replace(u' ', u'_') for itemname in itemnames]
        itemvalues[:] = [itemvalue.split(u'\xa0')[0] for itemvalue in itemvalues]

        print(filename)
        print(itemnames)
        print(itemvalues)
        # with open('output/' + filename, 'wb') as f:
        #    f.write(response.body)
        # self.log('Saved file %s' % filename)