"""
		self.matrix = []

		radius_vector = np.array([radius, radius])
		
		for y in xrange(0,grain):
			for x in xrange(0,grain):

				real_vector = np.array([x, y]) / float(grain)
				low = real_vector - radius_vector
				high = real_vector + radius_vector

				brightness = [0] * dataset.classes

				for sample in dataset.samples:
					features = sample.features
					cmp_vector = np.array([features[feature_x], features[feature_y]])

					if 	all(cmp_vector > low) and all(cmp_vector < high):
						distance = math.sqrt(sum(pow(cmp_vector - real_vector,2)))
						if distance < radius:
							brightness[sample.label] += radius - distance

				self.matrix += [brightness]
		maxi = np.amax(self.matrix, axis=0)
		self.matrix /= maxi
"""


"""
with open('datasets.csv', 'rb') as file:
	csvDataset = csv.reader(file, delimiter=',', quotechar='\'')
	for row in csvDataset:
		filename = row[0]
		dbname = row[1]
		dataset = Dataset('data/' + filename, dbname)
		print dataset
		chosen_lambda = [0,1]
		for x in xrange(0,15):
			exponer = Exponer(dataset, chosen_lambda, 30, 0.1)


"""
