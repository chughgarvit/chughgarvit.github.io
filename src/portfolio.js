const header = {
  // all the properties are optional - can be left empty or deleted
  homepage: '#about',
  title: 'GC.',
}

const about = {
  // all the properties are optional - can be left empty or deleted
  name: 'Garvit Chugh',
  role: 'PhD Scholar, Author, Entrepreneur',
  description: 'Result oriented, top performer, and self-starter professional with expertise in technologies such as mobile and wireless computing, IoT, Telecom Networks, software design, and operating systems. I work with sensors and IoT devices and make statistical analysis to find data-driven solutions and perform data visualization. Currently a Ph.D. scholar at IIT Jodhpur under the supervision of Dr. Suchetana Chakraborty, and Dr. Sandip Chakraborty, IIT Kharagpur',
  resume: 'https://drive.google.com/file/d/1MNL9R2CeONe07Y89kYmnT9gFgBcxQeT5/view?usp=sharing',
  social: {
    linkedin: 'https://www.linkedin.com/in/garvitchugh98/',
    github: 'https://github.com/chughgarvit',
    googlescholar: 'https://scholar.google.com/citations?user=15XfuxMAAAAJ&hl=en',
    dblp: 'https://dblp.org/pid/302/5075',
  },
}

const projects = [
  // projects can be added an removed
  // if there are no projects, Projects section won't show up
  {
    name: 'Quantifying attention using eSense (earable) devices ',
    description:
      'Using earable technology to detect the synchronized silent nodding of the listeners in an online meeting as the speaker speaks. And use it to quantify attention.',
    stack: ['Python3', 'scikit-learn', 'earables', 'HMM'],
    sourceCode: 'https://github.com',
  },
  {
    name: 'Ensemble based Intrusion detection system',
    description:
      'a technique is proposed that combines XGBoost with ensemble-based IDS to achieve a real time intrusion detection system',
    stack: ['Python3', 'Deep Learning'],
    sourceCode: 'https://github.com',
  },
  {
    name: 'Talk More',
    description:
      'Android-based application for real-time messaging, like WhatsApp',
    stack: ['Java', 'Android', 'Firebase', 'SQLite'],
    sourceCode: 'https://github.com',
  },
  {
    name: 'Legal Helper',
    description: 'Using image processing and classification to determine the meaning of a legal document like rental agreement, and presenting the meaning in a layman context.',
    stack: ['Java', 'Android', 'Firebase', 'SQLite', 'Computer Vision', 'Image Processing'],
    sourceCode: 'https://github.com',
  },
]

const skills = [
  // skills can be added or removed
  // if there are no skills, Skills section won't show up
  'C', 'C++', 'Java', 'Python', 'NodeJS', 'MySQL', 'Firebase', 'HTML', 'CSS', 'JavaScript', 'React', 'Material UI', 'Git',
  'Latex', 'Android Studio', 'NetBeans', 'Network Simulator (Version 3)',
  'Leadership', 'Problem Solving', 'Team Player', 'Communication Skills'
]

const contact = {
  // email is optional - if left empty Contact section won't show up
  email: 'chugh.2@iitj.ac.in',
}

const education = [
  {
    id: 1,
    title: "Doctor of Philosophy, Ph.D., (Mobile and Pervasive Computing)",
    location: "Indian Institute of Technology, Jodhpur, India",
    description:
      "Under the supervision of Dr. Suchetana Chakraborty, IIT Jodhpur, and Dr. Sandip Chakraborty, IIT Kharagpur.",
    buttonText: "View Frontend Projects",
    date: "January 2022 - present",
    icon: "school"
  },
  {
    id: 2,
    title: "Master of Technology, M.Tech, (CSE)",
    location: "Indian Institute of Technology, Jodhpur, India",
    description:
      "Under the supervision of Dr. Suchetana Chakraborty, IIT Jodhpur, and Dr. Sandip Chakraborty, IIT Kharagpur.",
    buttonText: "View Frontend Projects",
    date: "September 2020 - January 2022",
    icon: "school"
  },
  {
    id: 3,
    title: "Web Developer, Futural Solutions",
    location: "Delhi, India",
    description:
      "TestOnClick: A web-based solutions for taking online examinations. Later joined the start-up.",
    buttonText: "Company Website",
    date: "January 2020 - June 2020",
    icon: "work"
  },
  {
    id: 4,
    title: "Field Researcher, Futural Solutions",
    location: "Delhi, India",
    description:
      "GaliFoo: Find the exact location of street food vendors around you. Later joined the start-up, Collected data of the vendors throughout Delhi, and managed a team of 4",
    buttonText: "Course Certificate",
    date: "August 2019 - January 2020",
    icon: "work"
  },
  {
    id: 5,
    title: "Internships",
    location: "Delhi, India",
    description:
      "Android Developer (Internship), Airports Authority of India, AAI. Android Developer (Internship), Center for Railway Information Systems (CRIS)",
    buttonText: "College Projects",
    date: "June 2019 - August 2019",
    icon: "work"
  },
  {
    id: 6,
    title: "Bachelor of Technology, B.Tech, (CSE)",
    location: "Delhi-NCR, India",
    description:
      "Under the supervision of Dr. Bhoopesh Singh Bhati, NSUT, and Dr. Nitesh Singh Bhati, GGSIPU.",
    date: "2016 - 2020",
    icon: "school"
  }
]

export { header, about, projects, skills, contact, education }
