import React, {Component} from 'react';
import {Stage, Layer, Image, Circle} from 'react-konva';
import './App.css';
import useImage from 'use-image';
import Button from 'react-bootstrap/Button';
import Jumbotron from 'react-bootstrap/Jumbotron';
import Container from "react-bootstrap/Container";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
// the first very simple and recommended way:
let boardWidth = 870
let boardHeight = 600
let BoardImage = () => {
  const [image] = useImage('http://www.nonkit.com/smallbasic.files/Connect4Board.png');

  // return <Image image={image} width={window.innerWidth} height={window.innerHeight}/>;
  return <Image image={image} width={boardWidth} height={boardHeight}/>;
};


export default class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      play: true
    };
    this.handleClick = this.sendAction.bind(this);
  }


  startGamePlayer() {
    console.log("gameplayer")
    this.setState({play: true})
  }

  startGameBot() {
    console.log("gamebot")
    this.setState({play: true})
  }

  circlePos2(y, x) {
    let x0 = x * boardWidth / 7.1
    let y0 = y * boardHeight / 6
    let xstart = boardWidth / 13
    let ystart = boardHeight / 11.5
    console.log("Board w")
    console.log(boardWidth)
    console.log("Board h", boardHeight)
    return <Circle x={xstart + x0} y={ystart + y0} radius={45} fill={'red'} stroke={'black'} strokeWidth={4}/>
  }

  sendAction() {
    console.log("Send action")
  }

  render() {
    let gameGui;
    if (this.state.play) {
      var collumnButtons = []
      for (const id in [...Array(7).keys()]) {
        collumnButtons.push(<Col><Button onClick={() => this.sendAction(id)}>{id}</Button></Col>)
      }

      let board = <BoardImage/>

      console.log("Dup")
      console.log(board)
      let circles = [
        this.circlePos2(0, 0),
        this.circlePos2(1, 0),
        this.circlePos2(2, 0),
        this.circlePos2(1, 1),
        this.circlePos2(2, 2),
        this.circlePos2(3, 3),
        this.circlePos2(4, 4),
        this.circlePos2(5, 5),
      ]
      gameGui =
        <Container>
          <Row>
            {collumnButtons}
          </Row>
          <Stage width={window.innerWidth} height={window.innerHeight}>
            <Layer>
              {circles}
              {board}
            </Layer>
          </Stage>
        </Container>

    } else {
      gameGui = null
    }
    return (
      <Container className="p-3">
        <Jumbotron>
          <h1>Welcome To Connect4</h1>
          {this.state.play ?
            <Row><Col><Button
              onClick={() => this.setState({play: false})}
            >Reset</Button></Col></Row>
            : <Row>
              <Col><Button onClick={this.startGamePlayer.bind(this)}>New Game - Start Player</Button></Col>
              <Col><Button onClick={this.startGameBot.bind(this)}>New Game - Start Bot</Button></Col>
            </Row>
          }
        </Jumbotron>
        {gameGui}


      </Container>
    );
  }
}
