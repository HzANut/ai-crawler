

def generate_path(src_dir, website_list_file):
    parsed_list=[]
    with open(website_list_file, 'r') as file:
        lines = file.readlines()

        category = ''

        for line in lines:
            line = line.strip()

            if line.startswith('<'):
                continue

            if not line:
                continue

            parts = line.split()

            if len(parts) < 3:
                category = parts[0]
                continue

            site_abbr = parts[0]
            num_pages = parts[1]
            formatted_path = f'{src_dir}\\{category}\\{category}-{site_abbr}({num_pages})'

            parsed_list.append(formatted_path)

    return parsed_list


if __name__ ==  "__main__":
    print(generate_path(r"swde", "website_list.txt"))