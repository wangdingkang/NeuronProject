import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Scanner;
import java.util.Set;

import static java.nio.file.StandardCopyOption.*;

public class FileFunctions {

	public static void main(String[] args) throws IOException {
		for (int k = 1; k <= 5; k++) {
			String cellsFileFolder = "cell/";
			String kNNfile = "KNN/" + k + "NN.txt";
			String resultFile = "ret/classifyResult_density" + k + ".txt";
			int classNameDepth = 2;
			FileFunctions.validateSameDirectory(cellsFileFolder, kNNfile,
					resultFile, classNameDepth);
		}
		// String outputFolder = "data/Zhao_trees/NearestTreeFolder/";
		// copyNearestNeighborFile(fileFolder, NNCfile, outputFolder);
		// findNearestNeighborName(fileFolder, NNCfile, "28650283.swc");
		// CompareClassifyResults("data/Zhao_trees/output/classifyResult_persistance.txt","data/Zhao_trees/output/classifyResult_density.txt");
	}

	public static int kthIndexOf(String s, char c, int k) {
		for (int i = 0; i < s.length(); i++) {
			if (s.charAt(i) == c) {
				if (k == 1)
					return i;
				else
					k--;
			}
		}
		return -1;
	}

	/*
	 * validateSameDirectory checks how many trees within nearest neighbors of a
	 * tree is in the same class. cellsFileFolder path to folder contains all
	 * trees kNNFile path to the k nearest neighbor file output path to output
	 * file classNameDepth since tree classes are arranged hierarchically
	 * (subclasses are in the folder of parent classes), this variable specifies
	 * in which level we want to classify the trees.
	 */
	public static void validateSameDirectory(String cellsFileFolder,
			String kNNFile, String output, int classNameDepth)
			throws FileNotFoundException, UnsupportedEncodingException {
		List<String> fileNames = new LinkedList<String>();
		final File folder = new File(cellsFileFolder);
		FileFunctions.listFilesForFolder(folder, fileNames);

		int[] sameClass = new int[fileNames.size()];
		List<List<Integer>> nearestNeighborIndex = FileFunctions
				.readKNNList(kNNFile); // index start from 1

		// use map to save class name
		Map<String, Integer> classMap = new HashMap<String, Integer>(); // <class
																		// name,
																		// class
																		// size>
																		// pair
		// Map<String, String> nameFolder = new HashMap<String, String>();
		for (int i = 0; i < fileNames.size(); i++) {
			String queryName = fileNames.get(i);
			// String name = queryName.substring(0,
			// queryName.lastIndexOf("\\"));
			String name = queryName.substring(0,
					kthIndexOf(queryName, '\\', classNameDepth));
			// String fileName = queryName.substring(0,
			// queryName.lastIndexOf("\\")+1);
			if (!classMap.containsKey(name)) {
				classMap.put(name, 0);
			}
			classMap.put(name, classMap.get(name) + 1);
			// nameFolder.put(fileName, name);
		}
		for (int i = 0; i < nearestNeighborIndex.size(); i++) {
			for (int j = 0; j < nearestNeighborIndex.get(i).size(); j++) {
				int NNIndex = nearestNeighborIndex.get(i).get(j) - 1;
				String queryName = fileNames.get(i);
				String NNName = fileNames.get(NNIndex);
				// System.out.println(queryName+"\n"+NNName+"\n");
				if (queryName.substring(0,
						kthIndexOf(queryName, '\\', classNameDepth)).equals(
						NNName.substring(0,
								kthIndexOf(NNName, '\\', classNameDepth)))) {
					sameClass[i] += 1;
				}
			}
		}
		// check misclassified class size
		Map<String, Integer> misclassified = new LinkedHashMap<String, Integer>();
		for (int i = 0; i < fileNames.size(); i++) {
			if (sameClass[i] == 0) {
				String queryName = fileNames.get(i);
				String className = queryName.substring(0,
						kthIndexOf(queryName, '\\', classNameDepth));
				// String fileName = queryName.substring(0,
				// queryName.lastIndexOf("\\")+1);
				// TODO class count is not correct, fixed now 1/13/2016

				// System.out.println(queryName);

				if (!misclassified.containsKey(className)) {
					misclassified.put(className, 1);
				} else {
					misclassified.put(className,
							misclassified.get(className) + 1);
				}
			}
		}
		printList(sameClass, output);

		// print misclassified
		int[] bucket = new int[1000]; // TODO change class size if needed
		for (Map.Entry<String, Integer> entry : misclassified.entrySet()) {
			// if(classMap.get(entry.getKey()) == 1) continue;
			System.out.println(entry.getKey() + " : " + entry.getValue());
			bucket[classMap.get(entry.getKey())] += entry.getValue();
		}
		System.out.println("Statistics:");
		System.out.println("class size\tmisclassified count");
		for (int i = 0; i < bucket.length; i++) {
			if (bucket[i] > 0) {
				System.out.println(i + "\t\t" + bucket[i]);
			}
		}
		// TODO check first to make sure whether to include small size
		// classes!!! Use boundary var
		int boundary = 0;
		int sum = 0;
		int total = 0; // compute total number of trees that are in class with
						// size >= 5
		for (int i = 0; i < sameClass.length; i++) {
			String queryName = fileNames.get(i);
			String name = queryName.substring(0,
					kthIndexOf(queryName, '\\', classNameDepth));
			if (classMap.get(name) > boundary) {
				sum += sameClass[i] > 0 ? 1 : 0;
				total++;
			}
		}
		System.out.println(sum + "/" + total);

	}

	public static void findNearestNeighborName(String fileFolder, String input,
			String name) throws FileNotFoundException {
		System.out.println("find nearest neighbor for " + name + "...");
		List<String> fileNames = new LinkedList<String>();
		final File folder = new File(fileFolder);
		FileFunctions.listFilesForFolder(folder, fileNames);
		List<List<Integer>> nearestNeighborIndex = FileFunctions
				.readKNNList(input);
		int index = -1;
		for (int i = 0; i < fileNames.size(); i++) {
			String queryName = fileNames.get(i);
			String fileName = queryName
					.substring(queryName.lastIndexOf("\\") + 1);
			if (fileName.equals(name)) {
				index = i;
				break;
			}
		}
		if (index == -1) {
			return;
		}
		for (int i = 0; i < nearestNeighborIndex.get(index).size(); i++) {
			String neighborName = fileNames.get(nearestNeighborIndex.get(index)
					.get(i) - 1);
			String fileName = neighborName.substring(neighborName
					.lastIndexOf("\\") + 1);
			System.out.print(fileName + " ");
		}
	}

	public static void copyNearestNeighborFile(String fileFolder, String input,
			String outputFolder) throws IOException {
		System.out.println("copy nearest neighbor files...");
		List<String> fileNames = new LinkedList<String>();
		final File folder = new File(fileFolder);
		FileFunctions.listFilesForFolder(folder, fileNames);
		List<List<Integer>> nearestNeighborIndex = FileFunctions
				.readKNNList(input); // index start from 1
		for (int i = 0; i < nearestNeighborIndex.size(); i++) {
			String queryName = fileNames.get(i);
			String fileName = queryName
					.substring(queryName.lastIndexOf("\\") + 1);
			String subfolderPath = outputFolder + fileName + "/";
			boolean success = (new File(subfolderPath)).mkdirs();
			Path source = Paths.get(queryName);
			Path destination = Paths.get(subfolderPath + fileName);
			Files.copy(source, destination, REPLACE_EXISTING);
			for (int j = 0; j < nearestNeighborIndex.get(i).size(); j++) {
				String NNqueryName = fileNames.get(nearestNeighborIndex.get(i)
						.get(j) - 1);
				String NNfileName = NNqueryName.substring(NNqueryName
						.lastIndexOf("\\") + 1);
				Path NNsource = Paths.get(NNqueryName);
				Path NNdestination = Paths.get(subfolderPath + NNfileName);
				Files.copy(NNsource, NNdestination, REPLACE_EXISTING);
			}
		}
	}

	public static void printList(int[] sameClass, String output)
			throws FileNotFoundException, UnsupportedEncodingException {
		PrintWriter writer = new PrintWriter(output, "UTF-8");
		for (int i = 0; i < sameClass.length; i++) {
			writer.println(sameClass[i]);
		}
		writer.close();
	}

	public static List<List<Integer>> readKNNList(String input)
			throws FileNotFoundException {
		System.out.println("read Nearest Neighbor list...");
		List<List<Integer>> list = new ArrayList<List<Integer>>();
		Scanner scanner = new Scanner(new FileReader(input));
		while (scanner.hasNext()) {
			String[] nextLine = scanner.nextLine().split("\\s+");
			List<Integer> tmp = new ArrayList<Integer>();
			for (int i = 0; i < nextLine.length; i++) {
				tmp.add(Integer.parseInt(nextLine[i]));
			}
			list.add(tmp);
		}
		scanner.close();
		return list;
	}

	public static List<Integer> readList(String input)
			throws FileNotFoundException {
		List<Integer> list = new ArrayList<Integer>();
		Scanner scanner = new Scanner(new FileReader(input));
		while (scanner.hasNext()) {
			list.add(scanner.nextInt());
		}
		scanner.close();
		return list;
	}

	public static void listFilesForFolder(final File folder,
			List<String> fileNames) {
		for (final File fileEntry : folder.listFiles()) {
			if (fileEntry.isDirectory()) {
				listFilesForFolder(fileEntry, fileNames);
			} else {
				fileNames.add(fileEntry.getPath());
			}
		}
	}

	public static void deleteComment(List<String> fileNames, String outputFolder)
			throws FileNotFoundException {
		for (int i = 0; i < fileNames.size(); i++) {
			Scanner input = new Scanner(new FileReader(fileNames.get(i)));
			String line = "";
			while (!input.hasNextInt()) {
				input.nextLine();
			}
			File next = new File(fileNames.get(i));
			System.out.println(next.getName());
			String outputFile = outputFolder + next.getName();
			PrintWriter writer = new PrintWriter(outputFile);
			writer.println(line);
			while (input.hasNext()) {
				writer.println(input.nextLine());
			}
			input.close();
			writer.close();
		}
	}

	private static void extractNeuronFile(String fileName, String outputFolder,
			Set<Integer> structId, String prefix) throws FileNotFoundException {
		int rootStructID = 1;
		int index, structID, parentIndex, curIndex = 1;
		float x, y, z, radius;
		Map<Integer, Integer> indexMap = new HashMap<Integer, Integer>();
		File next = new File(fileName);
		Scanner input = new Scanner(next);
		String path = next.getPath();
		String name = next.getName();
		path = path.substring(0, path.length() - name.length());
		String outputFile = outputFolder + path + prefix + name;
		File p = new File(outputFolder + path);
		System.out.println(path + "\n" + outputFile);
		p.mkdirs();
		PrintWriter writer = new PrintWriter(outputFile);
		while (!input.hasNextInt()) {
			input.nextLine();
		}
		while (input.hasNext()) {
			index = input.nextInt();
			structID = input.nextInt();
			x = input.nextFloat();
			y = input.nextFloat();
			z = input.nextFloat();
			radius = input.nextFloat();
			parentIndex = input.nextInt();
			if (structID == rootStructID || structId.contains(structID)) {
				indexMap.put(index, curIndex);
				if (indexMap.containsKey(parentIndex)) {
					// node
					parentIndex = indexMap.get(parentIndex);
					writer.println(" " + curIndex + " " + structID + " " + x
							+ " " + y + " " + z + " " + radius + " "
							+ parentIndex);
				} else {
					// root
					writer.println(" " + curIndex + " " + structID + " " + x
							+ " " + y + " " + z + " " + radius + " " + "-1");
				}
				curIndex++;
			}
		}
		writer.close();
		input.close();
	}

	public static void copyAndBreak(List<String> fileNames, String outputFolder)
			throws FileNotFoundException {
		Set<Integer> axonIdSet = new HashSet<Integer>();
		axonIdSet.add(2);
		Set<Integer> dendriteIdSet = new HashSet<Integer>();
		dendriteIdSet.add(3);
		dendriteIdSet.add(4);
		for (int i = 0; i < fileNames.size(); i++) {

			extractNeuronFile(fileNames.get(i), outputFolder, axonIdSet,
					"axon_");
			extractNeuronFile(fileNames.get(i), outputFolder, dendriteIdSet,
					"dendrite_");
		}
	}

	public static boolean containsAllIds(String name, Set<Integer> keepIds)
			throws FileNotFoundException {
		File next = new File(name);
		Scanner input = new Scanner(next);
		int index, structID, parentIndex;
		float x, y, z, radius;
		while (input.hasNext()) {
			index = input.nextInt();
			structID = input.nextInt();
			x = input.nextFloat();
			y = input.nextFloat();
			z = input.nextFloat();
			radius = input.nextFloat();
			parentIndex = input.nextInt();
			keepIds.remove(structID);
			if (keepIds.size() == 0)
				break;
		}
		input.close();
		return keepIds.size() == 0;
	}

	public static void deleteOtherFile(List<String> fileNames,
			Set<Integer> keepIds) throws IOException {
		for (String name : fileNames) {
			Set<Integer> idCopy = new HashSet<Integer>(keepIds);
			if (containsAllIds(name, idCopy))
				continue;
			Files.delete(Paths.get(name));
		}
	}

	public static void CompareClassifyResults(String file1, String file2)
			throws FileNotFoundException {
		List<Integer> result1 = readList(file1);
		List<Integer> result2 = readList(file2);
		int count = 0;
		int total = 0;
		for (int i = 0; i < result1.size(); i++) {
			if (result1.get(i) == 0) {
				total++;
				if (result2.get(i) != 0) {
					count++;
				}
			}
		}
		System.out.println(count + "/" + total);
	}

}
