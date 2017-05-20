//============================================================================
// Name        : NTKNearestNeighbor.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C++, Ansi-style
//============================================================================

#include <iostream>
#include <vector>
#include <fstream>
#include <queue>
using namespace std;

typedef pair<double, int> myNN_pair;
struct Order
{
	bool operator()(myNN_pair const& a, myNN_pair const& b) const
	{
		return a.first < b.first;
	}
};

void readMat(string fileName,vector<vector<double> > &distanceMat){
	cerr << "Start reading matrix." << endl;
	std::ifstream ifs;
	ifs.open(fileName.c_str());
	unsigned int size;
	ifs>>size;
	ifs>>size;
	distanceMat.resize(size);
	for (size_t i = 0; i < size; ++i){
		distanceMat[i].resize(size);
	}
	double next;
	for(size_t i = 0;i<size;i++){
		for(size_t j = 0;j<size;j++){
			ifs>>next;
			distanceMat[i][j] = next;
		}
	}
	ifs.close();
	ifs.clear();
	cerr << "Reading finished." << endl;
}


void getNearestKNeighbor(string input, string output,  size_t k){
	cerr << "Calculating K neighbors." << endl;
	vector<vector<double> > distanceMat;
	readMat(input,distanceMat);
	vector<vector<int> > nearestNeighbor;
	nearestNeighbor.resize(distanceMat.size());
	for(size_t i = 0; i < distanceMat.size();i++){
		nearestNeighbor[i].resize(k);
	}
	for(size_t i = 0; i<distanceMat.size();i++){
		cerr << i << endl;
		std::priority_queue<myNN_pair, vector<myNN_pair>, Order > pq;
		for(size_t j = 0; j<distanceMat.size();j++){
			if(j == i) continue;
			pq.push(std::pair<double, int>(distanceMat[i][j], j+1));// file index start from 1.
			if(pq.size()>k) {
				pq.pop();
			}
		}
		for(size_t j = k-1;j>=0&&pq.size()>0;j--){
			nearestNeighbor[i][j] = pq.top().second;
			pq.pop();
		}
	}
	std::ofstream ofs;
	ofs.open(output.c_str());
	for(size_t i=0;i<nearestNeighbor.size();i++){
		for(size_t j = 0;j<k;j++){
			ofs<<nearestNeighbor[i][j]<<" ";
		}
		ofs<<"\n";
	}
	ofs.close();
	ofs.clear();
	cerr << "Finished." << endl;
}

int main(int argc, char **argv) {
	/*
	 * getNearestKNeighbor can compute the k nearest neighbors for every tree given their distance matrix.
	 *
	 * The variable distanceMatrixFile is the path to the distance matrix file.
	 * The kNNFile is the path to the result k nearest neighbors file.
	 * The k is the number of nearest neighbors we want.
	 *
	 * Please change these variables to satisfy your directory accordingly.
	 */
	string distanceMatrixFile = "data/distances.txt";
	string kNNFile = "data/kNN.txt";
	int k = 5;
	getNearestKNeighbor(distanceMatrixFile, kNNFile, k);
	return 0;
}
