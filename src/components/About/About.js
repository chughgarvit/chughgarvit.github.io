import GitHubIcon from '@material-ui/icons/GitHub'
import SchoolIcon from '@material-ui/icons/School'
import LinkedInIcon from '@material-ui/icons/LinkedIn'
import { Col, Container, Row } from 'react-bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css';
import myImage from '../../assets/myPic.jpg'
// import GoogleIcon from '@material-ui/icons/Google';

import { about } from '../../portfolio'
import './About.css'
import dblpIcon from '../../assets/dblp.png'


const About = () => {
  const { name, role, description, resume, social } = about

  return (
    <Container >
      <Row>
        <Col className='about' lg={{ span: 8, order: 1 }} md={{ span: 8, order: 1 }} xs={{ span: 12, order: 1 }} sm={{ span: 12, order: 1 }}>
          {name && (
            <div style={{ fontSize: "60px" }}>
              Hi, I am <span className='about__name'>{name}.</span>
            </div>
          )}

          {role && <h2 className='about__role'>A {role}.</h2>}
          <p className='about__desc'>{description && description}</p>

          <div className='about__contact center'>
            {resume && (
              <a href={resume}>
                <span type='button' className='btn btn--outline'>
                  Resume
                </span>
              </a>
            )}

            {social && (
              <>
                {social.github && (
                  <a
                    href={social.github}
                    aria-label='github'
                    className='link link--icon'
                  >
                    <GitHubIcon />
                  </a>
                )}

                {social.linkedin && (
                  <a
                    href={social.linkedin}
                    aria-label='linkedin'
                    className='link link--icon'
                  >
                    <LinkedInIcon />
                  </a>
                )}

                {social.googlescholar && (
                  <a
                    href={social.googlescholar}
                    aria-label='googlescholar'
                    className='link link--icon'
                  >
                    <SchoolIcon />
                  </a>
                )}

                {social.dblp && (
                  <a
                    href={social.dblp}
                    aria-label='dblp'
                    className='link link--icon'
                  >
                    <img src={dblpIcon} alt="DBLP" style={{ height: "28px", width: "28px" }} />
                  </a>
                )}

              </>
            )}
          </div>
        </Col>
        <Col lg={{ span: 4, order: 2 }} md={{ span: 4, order: 2 }} xs={{ span: 12, order: 2 }} sm={{ span: 12, order: 2 }}>

          <Row style={{ height: "10%" }} />
          <Row>
            <img src={myImage} alt="Logo" className="myImage center" />
          </Row>

        </Col>
      </Row>
    </Container>
  )
}

export default About
