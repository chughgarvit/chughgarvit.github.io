import { Container, Row } from 'react-bootstrap'
import uniqid from 'uniqid'
import React from 'react'
import { pubs } from '../../portfolio'
import PublicationsContainer from '../PublicationsContainer/PublicationsContainer'
import './Publications.css'


const Publications = () => {
  if (!pubs.length) return null

  return (
    <section id='publications' className='section publications'>
      <h2 className='section__title'>Publications</h2>

      <div className='publications__grid'>
        <ul className='listItem'>
          <li>
            Journals
          </li>
        </ul>
        <Container style={{ height: pubs.length * 90 }}>
          {pubs.map((publication) => (
            <div>
              <Row>
                <PublicationsContainer key={uniqid()} publication={publication} />
              </Row>
              <Row style={{ height: 20 }} />
            </div>
          ))}
        </Container>

        <ul className='listItem'>
          <li>
            Conferences
          </li>
        </ul>
        <Container style={{ height: pubs.length * 90 }}>
          {pubs.map((publication) => (
            <div>
              <Row>
                <PublicationsContainer key={uniqid()} publication={publication} />
              </Row>
              <Row style={{ height: 20 }} />
            </div>
          ))}
        </Container>


        <ul className='listItem'>
          <li>
            Book Chapters
          </li>
        </ul>
        <Container style={{ height: pubs.length * 90 }}>
          {pubs.map((publication) => (
            <div>
              <Row>
                <PublicationsContainer key={uniqid()} publication={publication} />
              </Row>
              <Row style={{ height: 20 }} />
            </div>
          ))}
        </Container>


        <ul className='listItem'>
          <li>
            Books
          </li>
        </ul>
        <Container style={{ height: pubs.length * 90 }}>
          {pubs.map((publication) => (
            <div>
              <Row>
                <PublicationsContainer key={uniqid()} publication={publication} />
              </Row>
              <Row style={{ height: 20 }} />
            </div>
          ))}
        </Container>


        <ul className='listItem'>
          <li>
            Patents
          </li>
        </ul>
        <Container style={{ height: pubs.length * 90 }}>
          {pubs.map((publication) => (
            <div>
              <Row>
                <PublicationsContainer key={uniqid()} publication={publication} />
              </Row>
              <Row style={{ height: 20 }} />
            </div>
          ))}
        </Container>

      </div >
    </section >
  )
}

export default Publications
