const header = {
  // all the properties are optional - can be left empty or deleted
  homepage: '#about',
  title: 'GC.',
}

const about = {
  // all the properties are optional - can be left empty or deleted
  name: 'Garvit Chugh',
  role: 'PhD Scholar, Entrepreneur, Author',
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
    livePreview: 'https://github.com',
  },
  {
    name: 'Ensemble based Intrusion detection system',
    description:
      'a technique is proposed that combines XGBoost with ensemble-based IDS to achieve a real time intrusion detection system',
    stack: ['Python3', 'Deep Learning'],
    sourceCode: 'https://github.com',
    livePreview: 'https://github.com',
  },
  {
    name: 'Talk More',
    description:
      'Android-based application for real-time messaging, like WhatsApp',
    stack: ['Java', 'Android', 'Firebase', 'SQLite'],
    sourceCode: 'https://github.com',
    livePreview: 'https://github.com',
  },
  {
    name: 'Legal Helper',
    description: 'Using image processing and classification to determine the meaning of a legal document like rental agreement, and presenting the meaning in a layman context.',
    stack: ['Java', 'Android', 'Firebase', 'SQLite', 'Computer Vision', 'Image Processing'],
    sourceCode: 'https://github.com',
    livePreview: 'https://github.com',
  },
]

const skills = [
  // skills can be added or removed
  // if there are no skills, Skills section won't show up
  'C', 'C++', 'Java', 'Python', 'NodeJS', 'MySQL', 'Firebase',
  'Latex', 'Android Studio', 'NetBeans', 'Network Simulator (Version 3)',

  'CSS',
  'JavaScript',
  'TypeScript',
  'React',
  'Redux',
  'Material UI',
  'Git',
  'Leadership', 'Problem Solving', 'Team Player', 'Communication Skills', 'HTML',
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
      "I work with sensors and IoT devices and make statistical analysis to find data-driven solutions and perform data visualization. Currently a Ph.D. scholar at IIT Jodhpur under the supervision of Dr. Suchetana Chakraborty, and Dr. Sandip Chakraborty, IIT Kharagpur",
    buttonText: "View Frontend Projects",
    date: "January 2022 - present",
    icon: "work"
  },
  {
    id: 2,
    title: "Backend Developer",
    location: "Skystead, Craonia",
    description:
      "Working hand-in-hand with front-end developers by providing the outward facing web application elements server-side logic. Creating the logic to make the web app function properly, and accomplishing this through the use of server-side scripting languages.",
    buttonText: "View Backend Projects",
    date: "June 2013 - August 2016",
    icon: "work"
  },
  {
    id: 3,
    title: "Quality Assurance Engineer",
    location: "South Warren, Geshington",
    description:
      "Assessing the quality of specifications and technical design documents in order to ensure timely, relevant and meaningful feedback.",
    buttonText: "Company Website",
    date: "September 2011 - June 2013",
    icon: "work"
  },
  {
    id: 4,
    title: "Oak Ridge College",
    location: "South Warren, Geshington",
    description:
      "Online Course in Magical Beasts and Wonders of the World - Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec scelerisque sagittis tellus, non ultrices lacus tempus vel.",
    buttonText: "Course Certificate",
    date: "September 2011",
    icon: "school"
  },
  {
    id: 5,
    title: "Hawking College",
    location: "Skystead, Craonia",
    description:
      "College - Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec scelerisque sagittis tellus, non ultrices lacus tempus vel.",
    buttonText: "College Projects",
    date: "2007 - 2011",
    icon: "school"
  },
  {
    id: 6,
    title: "Marble Hills Grammar School",
    location: "Dragontail, Ascana",
    description:
      "Highschool - Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec scelerisque sagittis tellus, non ultrices lacus tempus vel.",
    date: "2003 - 2007",
    icon: "school"
  }
]

export { header, about, projects, skills, contact, education }
