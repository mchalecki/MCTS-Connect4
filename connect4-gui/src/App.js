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

let backend_url = 'http://127.0.0.1:8000'
let boardWidth = 870
let boardHeight = 600
let boardYOffset = 60
let x_offset = (x) => x * boardWidth / 7.1
let y_offset = (y) => y * boardHeight / 6

let BoardImage = () => {
  const [image] = useImage('http://www.nonkit.com/smallbasic.files/Connect4Board.png');
  return <Image y={boardYOffset} image={image} width={boardWidth} height={boardHeight}/>;
};


export default class App extends Component {
  constructor(props) {
    super(props);
    this.state = App.initialState;
  }

  static get initialState() {
    return {
      board: null,
      terminal: null,
      winner: null,
      empty_field: null,
      legal_moves: null
    }
  }

  updateGameState(response) {
    let gameState = response.data
    console.log(gameState)
    this.setState({
      board: gameState.board,
      terminal: gameState.terminal,
      winner: gameState.winner,
      empty_field: gameState.empty_field,
      legal_moves: gameState.legal_moves,
    })
  }

  startGame(bot_starts) {
    axios.post(`${backend_url}/new_game/`, {
      bot_starts: bot_starts
    })
      .then(this.updateGameState.bind(this))
      .catch(console.log)
  }

  sendAction(row) {
    axios.post(`${backend_url}/make_move/`, {"row": row})
      .then(this.updateGameState.bind(this))
      .catch(console.log)
  }


  circlePos(y, x, color = "red") {
    let xstart = boardWidth / 13
    let ystart = boardYOffset + boardHeight / 11.5
    return <Circle x={xstart + x_offset(x)} y={ystart + y_offset(y)} radius={45} fill={color} stroke={'black'}
                   strokeWidth={4}/>
  }

  render() {
    let gameGui = null;

    if (this.state.board) {
      let konvaButtons = [];
      if (this.state.winner === null && this.state.legal_moves) {
        this.state.legal_moves.forEach(id => {
          konvaButtons.push(
            <Group x={40 + x_offset(id)} y={3} onClick={() => this.sendAction(id)}>
              <Rect strokeWidth={3} fill={"#ddd"} width={50} height={50} cornerRadius={10} stroke={"black"}
                    shadowColor={"black"} shadowBlur={10} shadowOffsetX={10} shadowOffsetY={10} shadowOpacity={0.2}
              />
              <Text x={15} y={15} text={id.toString()} fontSize={20} align={"center"} width={20}/>
            </Group>
          )
        })
      }

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
              <BoardImage/>

            </Layer>
          </Stage>
        </Container>
    }

    return (
      <Container className="p-3">
        <Jumbotron>
          <h1 align={"center"}>Welcome To Connect4</h1>
          {this.state.board ?
            <Row><Col><Button
              onClick={() => this.setState(App.initialState)}
            >Reset</Button></Col></Row>
            : <Row>
              <Col><Button onClick={() => this.startGame(false)}>New Game - Start Player</Button></Col>
              <Col><Button onClick={() => this.startGame(true)}>New Game - Start Bot</Button></Col>
            </Row>
          }
        </Jumbotron>
        {gameGui}
      </Container>
    );
  }
}
