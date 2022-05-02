import { Container, Row } from 'react-bootstrap'
import uniqid from 'uniqid'
import React from 'react'
import { journals, conferences, bookChapters, books, patents } from '../../pubPortfolio'
import PublicationsContainer from '../PublicationsContainer/PublicationsContainer'
import './Publications.css'


const Publications = () => (
  // Publications
  <section id='publications' className='section publications'>
    <h2 className='section__title'>Publications</h2>

    {/* Journals */}
    <div className='publications__grid'>
      <ul className='listItem'>
        <li>
          Journals
        </li>
      </ul>
      <Container style={{ height: journals.length * 90 }}>
        {journals.map((publication) => (
          <div>
            <Row>
              <PublicationsContainer key={uniqid()} publication={publication} />
            </Row>
            <Row style={{ height: 20 }} />
          </div>
        ))}
      </Container>

      {/* Conferences */}
      <ul className='listItem'>
        <li>
          Conferences
        </li>
      </ul>
      <Container style={{ height: conferences.length * 90 }}>
        {conferences.map((publication) => (
          <div>
            <Row>
              <PublicationsContainer key={uniqid()} publication={publication} />
            </Row>
            <Row style={{ height: 20 }} />
          </div>
        ))}
      </Container>

      {/* Book Chapters */}
      <ul className='listItem'>
        <li>
          Book Chapters
        </li>
      </ul>
      <Container style={{ height: bookChapters.length * 90 }}>
        {bookChapters.map((publication) => (
          <div>
            <Row>
              <PublicationsContainer key={uniqid()} publication={publication} />
            </Row>
            <Row style={{ height: 20 }} />
          </div>
        ))}
      </Container>

      {/* Books */}
      <ul className='listItem'>
        <li>
          Books
        </li>
      </ul>
      <Container style={{ height: books.length * 90 }}>
        {books.map((publication) => (
          <div>
            <Row>
              <PublicationsContainer key={uniqid()} publication={publication} />
            </Row>
            <Row style={{ height: 20 }} />
          </div>
        ))}
      </Container>

      {/* Patents */}
      <ul className='listItem'>
        <li>
          Patents
        </li>
      </ul>
      <Container style={{ height: patents.length * 90 }}>
        {patents.map((publication) => (
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

export default Publications
