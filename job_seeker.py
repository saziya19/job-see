import streamlit as st
import requests
from streamlit_lottie import st_lottie
# import time
from bs4 import BeautifulSoup

import openai
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from docx import Document
import gradio as gr
import re
import json
st.set_page_config(page_title="Job Finder",page_icon=":tada:",layout="wide")
st.markdown("""
<style>
.css-nqowgj.edgvbvh3
{
    visibility:hidden;
}
.css-164nlkn.egzxvld1
{
    visibility:hidden;
}
</style>
""",unsafe_allow_html=True)
def load_lottieurl(url):
    r=requests.get(url)
    if r.status_code!=200:
        return None
    return r.json()

lottie_coding = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_xbf1be8x.json")


with st.container():
    # st.title("Job Finder")
    st.markdown("<h1 style='text-align: center;'>Job Finder</h1>", unsafe_allow_html=True)
    st.subheader("Welcome to Job Finder")


with st.container():
    st.write("---")
    left_column,right_column = st.columns(2)
    with left_column:
        st.header("What I do")
        st.write("##")
        st.text(
            """
            On this Job Finder:\n
            \t People can easily find their suitable jobs in one location\n
            \tEnter the job description and get the suitable job positions
            
            """
        )

    with right_column:
        st_lottie(lottie_coding,height=300,key="coding")


with st.container():
    st.write("---")
    st.header("Job Search")
    st.write("##")
    description = st.text_area("Enter the description:")
    job =[]
    if st.button("Search"):
        # st.write("congratulations"+description)

        openai.api_key = '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'

            
        response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Get the job role, education , place , technologies , number of years of experience , job type from Description:\n{description}\n",
        
        temperature=0,
        max_tokens=100,
        n=1,
        stop=None,
        timeout=10,
        
        )

        main_summary = response.choices[0].text.strip()

        # print(main_summary)

        if main_summary != " ":       
            # Extract specific information using regular expressions
            job_role = re.search(r'Job Role:(.*)', main_summary).group(1).strip()
            education = re.search(r'Education:(.*)', main_summary).group(1).strip()
            place = re.search(r'Place:(.*)', main_summary).group(1).strip()
            technologies = re.search(r'Technologies:(.*)', main_summary).group(1).strip()
            experience = re.search(r'Experience:(.*)', main_summary).group(1).strip()
            job_type = re.search(r'Job Type:(.*)', main_summary).group(1).strip()

            # Create a dictionary for the summary
            summary_dict = {
                'Job_Role': job_role,
                'Education': education,
                'Place': place,
                'Technologies': technologies,
                'Experience': experience,
                'Job_Type': job_type,
            }

            # Print the summary dictionary
            print(summary_dict)
            print("SAZIYA")

            value1 = summary_dict.get("Job_Role")
            formatted_job_title = value1.replace(" ", "-")
            print(formatted_job_title)
            
           
            value2 = summary_dict.get("Education")
            value3 = summary_dict.get("Place")
            value4 = summary_dict.get("Technologies")
            value5_str = summary_dict.get("Experience")
            value6_str = summary_dict.get("Job_Type")

            url_parts = []
            url_parts2=[]
            url_parts3=[]
            url_parts4=[]
            url_parts5=[]
            
            

            if value1.lower() and value1.lower() not in ["n/a", "not specified", "none"]:
                stop_words = stopwords.words('english')
                stop_words.extend([","])
                tech_tokens = word_tokenize(value2)
                filtered_tech = [word for word in tech_tokens if word.lower() not in stop_words]
                filtered_tech_string = "-".join(filtered_tech).replace(" ","-").replace("/","-")
                
                url_parts.append(filtered_tech_string)

            if value2 and value2.lower() not in ["n/a", "not specified", "none"]:
                stop_words = stopwords.words('english')
                stop_words.extend([","])
                education_tokens = word_tokenize(value2)
                filtered_education = [word for word in education_tokens if word.lower() not in stop_words]
                filtered_education_string = "-".join(filtered_education).replace(" ","-").replace("/","-")
                url_parts5.append(filtered_education_string)

            if value3 and value3.lower() not in ["n/a", "not specified", "none"]:
                stop_words=stopwords.words('english')
                location=word_tokenize(value3)
                filtered_location=[word for word in location if word.lower() not in stop_words]
                filtered_location1='-'.join(filtered_location).replace(' ','-')
                url_parts4.append(filtered_location1)

            if value4 and value4.lower() not in ["n/a", "not specified", "none"]:
                stop_words = stopwords.words('english')
                stop_words.extend([","])
                technologies_tokens = word_tokenize(value4)
                filtered_technologies = [word for word in technologies_tokens if word.lower() not in stop_words]
                filtered_technologies_string = "-".join(filtered_technologies).replace(" ","-").replace("/","-")
                #formatted_job_title1=value4.replace(" ","-").replace("/","-")
                url_parts.append(filtered_technologies_string)
                
            if value5_str and value5_str.lower() not in ["n/a", "not specified", "none"]:
                years_match = re.search(r"\d+(\.\d+)?", value5_str)
                if years_match:
                    experience_num_str = years_match.group()
                    value5 = float(experience_num_str)
                    if value5 != 0:
                        if value5 < 5:
                            x = value5 * 12
                            url_parts2.append(str(int(x)))
                        else:
                            url_parts2.append("500")
                

            if url_parts and url_parts2 and url_parts3 and url_parts4 and url_parts5:
                joined_string2 = "-".join(url_parts3)
                joined_string = "-".join(url_parts)
                joined_string1 = "-".join(url_parts2)
                joined_string3 = "-".join(url_parts4)
                joined_string4 = "-".join(url_parts5)
                
                URL = f"https://www.freshersworld.com/jobs/jobsearch/{joined_string}-jobs-for-{joined_string4}-in-{joined_string3}?course=16&experience={joined_string1}&job_type={joined_string2}"
                lowercase_url = URL.lower()
                print(lowercase_url)
                response = requests.get(URL, allow_redirects=True)
                soup = BeautifulSoup(response.content, 'html.parser')
                job_listings = soup.find_all('div', class_='job-container')
                search_criteria = " "
                relevant_jobs = []
                for job in job_listings:
                    job_title = job.find('span', class_='wrap-title').text
                    company_name = job.find('h3', class_='latest-jobs-title font-16 margin-none inline-block company-name').text
                    job_location = job.find('span', class_='job-location display-block modal-open job-details-span').text
                    qualifications = job.find('span', class_='qualifications display-block modal-open pull-left job-details-span').text
                    
                    view_apply_button = job.find('span', class_='view-apply-button')
                    view_apply_link = ''
                    if view_apply_button:
                     parent_div = view_apply_button.find_parent('div', class_='job-container')
                     if parent_div:
                        view_apply_link = parent_div.get('job_display_url', '')
                    if all(keyword in value1.lower() or keyword in value5.lower() or keyword in value6_str.lower()or keyword in value3.lower() or keyword in value2 for keyword in search_criteria.lower().split()):
                         relevant_job = {
                        'job_title': job_title[:-4].rstrip(),
                        'company_name': company_name,
                        'job_location': job_location,
                        'qualifications': qualifications,
                    }
                    relevant_jobs.append(relevant_job)
                for job in relevant_jobs:
                    st.subheader(job['job_title'])
                    st.write(job['company_name'])
                    st.write(job['job_location'])
                    st.write(job['qualifications'])
                    st.markdown(f'<a href="{view_apply_link}" target="_blank" rel="noopener noreferrer" ><button>Apply</button></a>', unsafe_allow_html=True)
                    st.write("---")
                
                
            elif url_parts and url_parts2 and url_parts3 and url_parts4:
                joined_string2 = "-".join(url_parts3)
                joined_string = "-".join(url_parts)
                joined_string1 = "-".join(url_parts2)
                joined_string3 = "-".join(url_parts4)
                URL = f"https://www.freshersworld.com/jobs/jobsearch/{joined_string}-jobs-in-{joined_string3}?course=16&experience={joined_string1}&job_type={joined_string2}"
                lowercase_url = URL.lower()
                lowercase_url.replace('/','-')
                print(lowercase_url)
                response = requests.get(URL, allow_redirects=True)
                soup = BeautifulSoup(response.content, 'html.parser')
                job_listings = soup.find_all('div', class_='job-container')
                search_criteria = " "
                relevant_jobs = []
                for job in job_listings:
                    job_title = job.find('span', class_='wrap-title').text
                    company_name = job.find('h3', class_='latest-jobs-title font-16 margin-none inline-block company-name').text
                    job_location = job.find('span', class_='job-location display-block modal-open job-details-span').text
                    qualifications = job.find('span', class_='qualifications display-block modal-open pull-left job-details-span').text
                    
                    view_apply_button = job.find('span', class_='view-apply-button')
                    view_apply_link = ''
                    if view_apply_button:
                     parent_div = view_apply_button.find_parent('div', class_='job-container')
                     if parent_div:
                        view_apply_link = parent_div.get('job_display_url', '')
                    if all(keyword in value1.lower() or keyword in value5.lower() or keyword in value6_str.lower()or keyword in value3.lower() for keyword in search_criteria.lower().split()):
                         relevant_job = {
                        'job_title': job_title[:-4].rstrip(),
                        'company_name': company_name,
                        'job_location': job_location,
                        'qualifications': qualifications,
                    }
                    relevant_jobs.append(relevant_job)
                for job in relevant_jobs:
                    st.subheader(job['job_title'])
                    st.write(job['company_name'])
                    st.write(job['job_location'])
                    st.write(job['qualifications'])
                    st.markdown(f'<a href="{view_apply_link}" target="_blank" rel="noopener noreferrer" ><button>Apply</button></a>', unsafe_allow_html=True)
                    st.write("---")
            elif url_parts and url_parts4 and url_parts2:
                joined_string = "-".join(url_parts)
                joined_string1 = "-".join(url_parts2)
                joined_string3 = "-".join(url_parts4)
                URL = f"https://www.freshersworld.com/jobs/jobsearch/{joined_string}-jobs-in-{joined_string3}?course=16&experience={joined_string1}"
                lowercase_url = URL.lower()
                print(lowercase_url)
                response = requests.get(URL, allow_redirects=True)
                soup = BeautifulSoup(response.content, 'html.parser')
                job_listings = soup.find_all('div', class_='job-container')
                search_criteria = " "
                relevant_jobs = []
                for job in job_listings:
                    job_title = job.find('span', class_='wrap-title').text
                    company_name = job.find('h3', class_='latest-jobs-title font-16 margin-none inline-block company-name').text
                    job_location = job.find('span', class_='job-location display-block modal-open job-details-span').text
                    qualifications = job.find('span', class_='qualifications display-block modal-open pull-left job-details-span').text
                    
                    view_apply_button = job.find('span', class_='view-apply-button')
                    view_apply_link = ''
                    if view_apply_button:
                     parent_div = view_apply_button.find_parent('div', class_='job-container')
                     if parent_div:
                        view_apply_link = parent_div.get('job_display_url', '')
                    if all(keyword in value1.lower() or keyword in value3.lower() or keyword in value5.lower() for keyword in search_criteria.lower().split()):
                         relevant_job = {
                        'job_title': job_title[:-4].rstrip(),
                        'company_name': company_name,
                        'job_location': job_location,
                        'qualifications': qualifications,
                    }
                    relevant_jobs.append(relevant_job)
                for job in relevant_jobs:
                    st.subheader(job['job_title'])
                    st.write(job['company_name'])
                    st.write(job['job_location'])
                    st.write(job['qualifications'])
                    st.markdown(f'<a href="{view_apply_link}" target="_blank" rel="noopener noreferrer" ><button>Apply</button></a>', unsafe_allow_html=True)
                    st.write("---")
               
            elif url_parts and url_parts2 and url_parts3:
                joined_string2 = "-".join(url_parts3)
                joined_string = "-".join(url_parts)
                joined_string1 = "-".join(url_parts2)
                URL = f"https://www.freshersworld.com/jobs/jobsearch/{joined_string}-jobs?course=16&experience={joined_string1}&job_type={joined_string2}"
                lowercase_url = URL.lower()
                print(lowercase_url)
                response = requests.get(URL, allow_redirects=True)
                soup = BeautifulSoup(response.content, 'html.parser')
                job_listings = soup.find_all('div', class_='job-container')
                search_criteria = " "
                relevant_jobs = []
                for job in job_listings:
                    job_title = job.find('span', class_='wrap-title').text
                    company_name = job.find('h3', class_='latest-jobs-title font-16 margin-none inline-block company-name').text
                    job_location = job.find('span', class_='job-location display-block modal-open job-details-span').text
                    qualifications = job.find('span', class_='qualifications display-block modal-open pull-left job-details-span').text
                    
                    view_apply_button = job.find('span', class_='view-apply-button')
                    view_apply_link = ''
                    if view_apply_button:
                     parent_div = view_apply_button.find_parent('div', class_='job-container')
                     if parent_div:
                        view_apply_link = parent_div.get('job_display_url', '')
                    if all(keyword in value1.lower() or keyword in value5.lower() or keyword in value6_str.lower() for keyword in search_criteria.lower().split()):
                         relevant_job = {
                        'job_title': job_title[:-4].rstrip(),
                        'company_name': company_name,
                        'job_location': job_location,
                        'qualifications': qualifications,
                    }
                    relevant_jobs.append(relevant_job)
                for job in relevant_jobs:
                    st.subheader(job['job_title'])
                    st.write(job['company_name'])
                    st.write(job['job_location'])
                    st.write(job['qualifications'])
                    st.markdown(f'<a href="{view_apply_link}" target="_blank" rel="noopener noreferrer" ><button>Apply</button></a>', unsafe_allow_html=True)
                    st.write("---")
                
            elif url_parts and url_parts4 :
                joined_string = "-".join(url_parts)
                joined_string3 = "-".join(url_parts4)
                URL = f"https://www.freshersworld.com/jobs/jobsearch/{joined_string}-jobs-in-{joined_string3}?course=16"
                lowercase_url = URL.lower()
                print(lowercase_url)
                response = requests.get(URL, allow_redirects=True)
                soup = BeautifulSoup(response.content, 'html.parser')
                job_listings = soup.find_all('div', class_='job-container')
                search_criteria = " "
                relevant_jobs = []
                for job in job_listings:
                    job_title = job.find('span', class_='wrap-title').text
                    company_name = job.find('h3', class_='latest-jobs-title font-16 margin-none inline-block company-name').text
                    job_location = job.find('span', class_='job-location display-block modal-open job-details-span').text
                    qualifications = job.find('span', class_='qualifications display-block modal-open pull-left job-details-span').text
                    
                    view_apply_button = job.find('span', class_='view-apply-button')
                    view_apply_link = ''
                    if view_apply_button:
                     parent_div = view_apply_button.find_parent('div', class_='job-container')
                     if parent_div:
                        view_apply_link = parent_div.get('job_display_url', '')
                    if all(keyword in value1.lower() or keyword in value3.lower() for keyword in search_criteria.lower().split()):
                         relevant_job = {
                        'job_title': job_title[:-4].rstrip(),
                        'company_name': company_name,
                        'job_location': job_location,
                        'qualifications': qualifications,
                    }
                    relevant_jobs.append(relevant_job)
                for job in relevant_jobs:
                    st.subheader(job['job_title'])
                    st.write(job['company_name'])
                    st.write(job['job_location'])
                    st.write(job['qualifications'])
                    st.markdown(f'<a href="{view_apply_link}" target="_blank" rel="noopener noreferrer" ><button>Apply</button></a>', unsafe_allow_html=True)
                    st.write("---")
                
                

            elif url_parts and url_parts2:
               joined_string = "-".join(url_parts)
               joined_string1 = "-".join(url_parts2)
               URL = f"https://www.freshersworld.com/jobs/jobsearch/{joined_string}-jobs?experience={joined_string1}"
               lowercase_url = URL.lower()
               print(lowercase_url)
               response = requests.get(URL, allow_redirects=True)
               soup = BeautifulSoup(response.content, 'html.parser')
               job_listings = soup.find_all('div', class_='job-container')
               search_criteria = " "
               relevant_jobs = []
               for job in job_listings:
                    job_title = job.find('span', class_='wrap-title').text
                    company_name = job.find('h3', class_='latest-jobs-title font-16 margin-none inline-block company-name').text
                    job_location = job.find('span', class_='job-location display-block modal-open job-details-span').text
                    qualifications = job.find('span', class_='qualifications display-block modal-open pull-left job-details-span').text
                    
                    view_apply_button = job.find('span', class_='view-apply-button')
                    view_apply_link = ''
                    if view_apply_button:
                     parent_div = view_apply_button.find_parent('div', class_='job-container')
                     if parent_div:
                        view_apply_link = parent_div.get('job_display_url', '')
                    if all(keyword in value1.lower() or keyword in value5.lower() for keyword in search_criteria.lower().split()):
                         relevant_job = {
                        'job_title': job_title[:-4].rstrip(),
                        'company_name': company_name,
                        'job_location': job_location,
                        'qualifications': qualifications,
                    }
                    relevant_jobs.append(relevant_job)
               for job in relevant_jobs:
                    st.subheader(job['job_title'])
                    st.write(job['company_name'])
                    st.write(job['job_location'])
                    st.write(job['qualifications'])
                    st.markdown(f'<a href="{view_apply_link}" target="_blank" rel="noopener noreferrer" ><button>Apply</button></a>', unsafe_allow_html=True)
                    st.write("---")
            elif  url_parts2:
                joined_string1 = "-".join(url_parts2)
                
                URL = f"https://www.freshersworld.com/jobs/jobsearch/?experience={joined_string1}"
                lowercase_url = URL.lower()
                print(lowercase_url)
                response = requests.get(URL, allow_redirects=True)
                soup = BeautifulSoup(response.content, 'html.parser')
                job_listings = soup.find_all('div', class_='job-container')
                search_criteria = " "
                relevant_jobs = []
                for job in job_listings:
                    job_title = job.find('span', class_='wrap-title').text
                    company_name = job.find('h3', class_='latest-jobs-title font-16 margin-none inline-block company-name').text
                    job_location = job.find('span', class_='job-location display-block modal-open job-details-span').text
                    qualifications = job.find('span', class_='qualifications display-block modal-open pull-left job-details-span').text
                    
                    view_apply_button = job.find('span', class_='view-apply-button')
                    view_apply_link = ''
                    if view_apply_button:
                     parent_div = view_apply_button.find_parent('div', class_='job-container')
                     if parent_div:
                        view_apply_link = parent_div.get('job_display_url', '')
                    if all(keyword in value5.lower() for keyword in search_criteria.lower().split()):
                         relevant_job = {
                        'job_title': job_title[:-4].rstrip(),
                        'company_name': company_name,
                        'job_location': job_location,
                        'qualifications': qualifications,
                    }
                    relevant_jobs.append(relevant_job)
                for job in relevant_jobs:
                    st.subheader(job['job_title'])
                    st.write(job['company_name'])
                    st.write(job['job_location'])
                    st.write(job['qualifications'])
                    st.markdown(f'<a href="{view_apply_link}" target="_blank" rel="noopener noreferrer" ><button>Apply</button></a>', unsafe_allow_html=True)
                    st.write("---")
                
         
            elif  url_parts4:
                joined_string3 = "-".join(url_parts4)
                
                URL = f"https://www.freshersworld.com/jobs/jobsearch/jobs-in-{joined_string3}"
                lowercase_url = URL.lower()
                print(lowercase_url)
                response = requests.get(URL, allow_redirects=True)
                soup = BeautifulSoup(response.content, 'html.parser')
                job_listings = soup.find_all('div', class_='job-container')
                search_criteria = " "
                relevant_jobs = []
                for job in job_listings:
                    job_title = job.find('span', class_='wrap-title').text
                    company_name = job.find('h3', class_='latest-jobs-title font-16 margin-none inline-block company-name').text
                    job_location = job.find('span', class_='job-location display-block modal-open job-details-span').text
                    qualifications = job.find('span', class_='qualifications display-block modal-open pull-left job-details-span').text
                    
                    view_apply_button = job.find('span', class_='view-apply-button')
                    view_apply_link = ''
                    if view_apply_button:
                     parent_div = view_apply_button.find_parent('div', class_='job-container')
                     if parent_div:
                        view_apply_link = parent_div.get('job_display_url', '')
                    if all(keyword in value3.lower() for keyword in search_criteria.lower().split()):
                         relevant_job = {
                        'job_title': job_title[:-4].rstrip(),
                        'company_name': company_name,
                        'job_location': job_location,
                        'qualifications': qualifications,
                    }
                    relevant_jobs.append(relevant_job)
                for job in relevant_jobs:
                    st.subheader(job['job_title'])
                    st.write(job['company_name'])
                    st.write(job['job_location'])
                    st.write(job['qualifications'])
                    st.markdown(f'<a href="{view_apply_link}" target="_blank" rel="noopener noreferrer" ><button>Apply</button></a>', unsafe_allow_html=True)
                    st.write("---")
                
            elif  url_parts5:
                joined_string4 = "-".join(url_parts5)
                
                URL = f"https://www.freshersworld.com/jobs/jobsearch/jobs-for-{joined_string4}"
                lowercase_url = URL.lower()
                print(lowercase_url)
                response = requests.get(URL, allow_redirects=True)
                soup = BeautifulSoup(response.content, 'html.parser')
                job_listings = soup.find_all('div', class_='job-container')
                search_criteria = " "
                relevant_jobs = []
                for job in job_listings:
                    job_title = job.find('span', class_='wrap-title').text
                    company_name = job.find('h3', class_='latest-jobs-title font-16 margin-none inline-block company-name').text
                    job_location = job.find('span', class_='job-location display-block modal-open job-details-span').text
                    qualifications = job.find('span', class_='qualifications display-block modal-open pull-left job-details-span').text
                    
                    view_apply_button = job.find('span', class_='view-apply-button')
                    view_apply_link = ''
                    if view_apply_button:
                     parent_div = view_apply_button.find_parent('div', class_='job-container')
                     if parent_div:
                        view_apply_link = parent_div.get('job_display_url', '')
                    if all(keyword in value2.lower() for keyword in search_criteria.lower().split()):
                         relevant_job = {
                        'job_title': job_title[:-4].rstrip(),
                        'company_name': company_name,
                        'job_location': job_location,
                        'qualifications': qualifications,
                    }
                    relevant_jobs.append(relevant_job)
                for job in relevant_jobs:
                    st.subheader(job['job_title'])
                    st.write(job['company_name'])
                    st.write(job['job_location'])
                    st.write(job['qualifications'])
                    st.markdown(f'<a href="{view_apply_link}" target="_blank" rel="noopener noreferrer" ><button>Apply</button></a>', unsafe_allow_html=True)
                    st.write("---")
                
            
            
            
            elif  url_parts:
                joined_string = "-".join(url_parts)
                
                URL = f"https://www.freshersworld.com/jobs/jobsearch/{joined_string}"
                lowercase_url = URL.lower()
                print(lowercase_url)
                response = requests.get(URL, allow_redirects=True)
                soup = BeautifulSoup(response.content, 'html.parser')
                job_listings = soup.find_all('div', class_='job-container')
                search_criteria = " "
                relevant_jobs = []
                for job in job_listings:
                    job_title = job.find('span', class_='wrap-title').text
                    company_name = job.find('h3', class_='latest-jobs-title font-16 margin-none inline-block company-name').text
                    job_location = job.find('span', class_='job-location display-block modal-open job-details-span').text
                    qualifications = job.find('span', class_='qualifications display-block modal-open pull-left job-details-span').text
                    
                    view_apply_button = job.find('span', class_='view-apply-button')
                    view_apply_link = ''
                    if view_apply_button:
                     parent_div = view_apply_button.find_parent('div', class_='job-container')
                     if parent_div:
                        view_apply_link = parent_div.get('job_display_url', '')
                    if all(keyword in value1.lower() or keyword in value4.lower() for keyword in search_criteria.lower().split()):
                         relevant_job = {
                        'job_title': job_title[:-4].rstrip(),
                        'company_name': company_name,
                        'job_location': job_location,
                        'qualifications': qualifications,
                    }
                    relevant_jobs.append(relevant_job)
                for job in relevant_jobs:
                    st.subheader(job['job_title'])
                    st.write(job['company_name'])
                    st.write(job['job_location'])
                    st.write(job['qualifications'])
                    st.markdown(f'<a href="{view_apply_link}" target="_blank" rel="noopener noreferrer" ><button>Apply</button></a>', unsafe_allow_html=True)
                    st.write("---")
                    
            else:
                print("No valid information provided to generate the URL.")
                