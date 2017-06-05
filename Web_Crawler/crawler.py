import scrapy
import os
import re

base_url = 'http://neuromorpho.org/neuron_info.jsp?neuron_name='
neuron_folder = 'neurons\\'
output_folder = 'crawled\\'

class LFeatureSpider(scrapy.Spider):
    name = "l-feature"
    urls = []
    filepaths = []

    def read_in_all_neurons(self):
        for root, dirs, files in os.walk(neuron_folder, topdown=False):
            for name in files:
                print(os.path.join(root, name))
                # origin = os.path.join(root, name)
                self.filepaths.append(os.path.join(output_folder, root[root.find('\\')+1:] + '\\' + name.split('.')[0] + '.txt'))
                self.urls.append(base_url + name.split('.')[0])

    def start_requests(self):
        self.read_in_all_neurons()
        for url, filepath in zip(self.urls, self.filepaths):
            yield scrapy.Request(url=url, callback=self.parse, meta={'pos' : filepath})

    def parse(self, response):
        # name = response.url.split("=")[-1]
        filename = response.meta['pos'];
        info = response.css('table[id=NeuronInfotable11]')
        itemnames = info.css('td[align=right]::text').extract()[1:]
        itemvalues = info.css('td[align=left]::text').extract()[1:]

        itemnames[:] = [re.sub('[^a-zA-z0-9\.]', '', itemname) for itemname in itemnames]
        itemvalues[:] = [re.sub('[^0-9\.]', '', itemvalue) for itemvalue in itemvalues]

        # print(filename)
        # print(itemnames)
        # print(itemvalues)
        dir_path = filename[:filename.rfind('\\')]
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        # print(dir_path)

        with open(filename, 'w') as f:
            for itemname, itemvalue in zip(itemnames, itemvalues):
                f.write(itemname + " " + itemvalue + '\n')

        self.log('Saved file %s' % filename)


# if __name__ == '__main__':
#     for root, dirs, files in os.walk(neuron_folder, topdown=False):
#         for name in files:
#             print(os.path.join(root, name))
#             # origin = os.path.join(root, name)
#             print(os.path.join(output_folder, root[root.find('\\') + 1:] + '\\' + name.split('.')[0] + '.txt'))
#             print(base_url + name.split('.')[0])