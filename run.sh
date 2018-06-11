## declare an array variable
declare -a keywords=("Digital marketing companies" "Online marketing companies" "Website development companies" "Inbound Marketing company" "Social Media Marketing company" "SEO company"  "Search Engine Optimisation company" "Google adwords online advertising services" "Facebook marketing company" "Social media marketing")
declare -a cities=("Mumbai" "Pune" "Goregaon" "Andheri" "Bandra" "Powai, Mumbai" "Juhu , Mumbai")

## now loop through the above array
for i in "${keywords[@]}"
do
	for j in "${cities[@]}"
	do
		python email_new_blog.py "$i in $j"
	done
   # or do whatever with individual element of the array
done

# "Digital marketing bloggers" "tech blogs" "sales marketing blogs" "inbound marketing blogs" "top marketing blogs" "email marketing blogs" "seo marketing blog"

