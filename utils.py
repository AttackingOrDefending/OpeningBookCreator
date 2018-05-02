import os
import yaml
import urllib.request

def create_dir(path):
	if not os.path.exists(path):
		os.makedirs(path)
		print("created directory {}".format(path))
	else:
		#print("{} exists".format(path))
		pass

def write_string_to_file(path, str, force = True):
	if os.path.isfile(path) and not force:
		return
	with open(path,"w") as outfile:
		outfile.write(str)
	print("written file {} ( {} characters )".format(path,len(str)))

def load_yaml(path):
	try:
		with open(path, 'r') as stream:
			try:
				obj = yaml.load(stream)
				return obj
			except Exception as e:
				return {}
	except:
		return {}

def dump_yaml(path, obj):
	write_string_to_file(path,yaml.dump(obj))

def store_url(url, path):
	with urllib.request.urlopen(url) as response, open(path, 'wb') as out_file:
		data = response.read()
		out_file.write(data)
		print("retrieved {} to {} ( {} bytes )".format(url,path,len(data)))


