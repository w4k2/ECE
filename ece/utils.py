def getType(value):
	tests = [(int, int),(float, float),(str,str)]
	for typ, test in tests:
		try:
			test(value)
			return typ
		except ValueError:
			continue
			return None