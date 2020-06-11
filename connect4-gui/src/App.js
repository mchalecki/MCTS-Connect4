import React, {Component} from 'react';
import {Stage, Layer, Image, Circle, Text, Rect, Group} from 'react-konva';
import './App.css';
import useImage from 'use-image';
import Button from 'react-bootstrap/Button';
import Jumbotron from 'react-bootstrap/Jumbotron';
import Container from "react-bootstrap/Container";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import axios from 'axios';

let boardWidth = 870
let boardHeight = 600
let boardYOffset = 60
let BoardImage = () => {
  const [image] = useImage('http://www.nonkit.com/smallbasic.files/Connect4Board.png');

  // return <Image image={image} width={window.innerWidth} height={window.innerHeight}/>;
  return <Image y={boardYOffset} image={image} width={boardWidth} height={boardHeight}/>;
};


export default class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      play: false,
      board: null,
      terminal: null,
      winner: null,
      empty_field: null,
    };
  }


  startGamePlayer() {
    axios.post('http://localhost:8000/new_game', {
      bot_starts: false
    })
      .then(function (response) {
          this.setState({
            board: response.data.board,
            terminal: response.data.terminal,
            winner: response.data.winner,
            empty_field: response.data.empty_field
          })
        }.bind(this)
      )
      .catch(function (error) {
        console.log(error);
      })
    this.setState({play: true})
  }

  startGameBot() {
    axios.post('http://127.0.0.1:8000/new_game', {})
      .then(function (response) {
        this.setState({
          board: response.data.board,
          terminal: response.data.terminal,
          winner: response.data.winner,
          empty_field: response.data.empty_field
        })
        console.log(response.data.board)
      }.bind(this))
      .catch(function (error) {
        console.log(error);
      });
    this.setState({play: true})
  }

  circlePos(y, x, color = "red") {
    let x0 = x * boardWidth / 7.1
    let y0 = y * boardHeight / 6
    let xstart = boardWidth / 13
    let ystart = boardYOffset + boardHeight / 11.5
    return <Circle x={xstart + x0} y={ystart + y0} radius={45} fill={color} stroke={'black'}
                   strokeWidth={4}/>
  }

  sendAction(row) {
    axios.post('http://127.0.0.1:8000/make_move', {"row": row})
      .then(function (response) {
        this.setState({board: response.data.board, terminal: response.data.terminal, winner: response.data.winner})
      }.bind(this))
      .catch(function (error) {
        console.log(error);
      });
    this.setState({play: true})
  }

  render() {
    let gameGui;
    if (this.state.play) {
      let konvaButtons = [];
      if (this.state.winner === null) {
        for (const id in [...Array(7).keys()]) {
          konvaButtons.push(
            <Group x={40 + (boardWidth / 7.1 * id)} y={3} onClick={() => this.sendAction(id)}>
              <Rect strokeWidth={3} fill={"#ddd"} width={50} height={50} cornerRadius={10} stroke={"black"}
                    shadowColor={"black"} shadowBlur={10} shadowOffsetX={10} shadowOffsetY={10} shadowOpacity={0.2}
              />
              <Text x={15} y={15} text={id.toString()} fontSize={20} align={"center"} width={20}/>
            </Group>
          )
        }
      }


      let board = <BoardImage/>
      let circles = []
      if (this.state.board) {
        this.state.board.forEach((row, row_idx) => row.forEach(
          (col, col_idx) => {
            if (col !== this.state.empty_field) {
              circles.push(this.circlePos(row_idx, col_idx, col === 1 ? "red" : "yellow"))
            }
          }
        ))
      }

      gameGui =
        <Container>
          {this.state.winner !== null &&
            <h1 align={"center"}>Winner is {this.state.winner === 1 ? "red" : "yellow"}</h1>
          }
          <Stage width={window.innerWidth} height={window.innerHeight}>
            <Layer>
              {konvaButtons}
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
          <h1 align={"center"}>Welcome To Connect4</h1>
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
