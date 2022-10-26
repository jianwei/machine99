import yaml

def get_yaml_data(yaml_file):
    with open(yaml_file, encoding='utf-8')as file:
        content = file.read()
        data = yaml.load(content, Loader=yaml.FullLoader)
        return data

if __name__ == "__main__":
    data=get_yaml_data("config.yaml")
    print(data.get('unix_socket')) 