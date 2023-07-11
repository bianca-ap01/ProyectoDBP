<template>
  <main class="app">
    <h1>{{ title }}</h1>

    <section class="quiz" v-if="!quizCompleted">
      <div class="quiz-info">
        <span class="question">{{ getCurrentQuestion.question }}</span>
        <span class="score">Score {{ score }}/{{ questions.length }}</span>
      </div>

      <div class="options">
        <label
          v-for="(option, index) in getCurrentQuestion.options"
          :key="option.id"
          :for="'option' + index"
          :class="`option ${
            getCurrentQuestion.selected == index
              ? index == getCurrentQuestion.answer
                ? 'correct'
                : 'wrong'
              : ''
          } ${
            getCurrentQuestion.selected != null &&
            index != getCurrentQuestion.selected
              ? 'disabled'
              : ''
          }`"
        >
          <input
            type="radio"
            :id="'option' + index"
            :name="getCurrentQuestion.index"
            :value="index"
            v-model="getCurrentQuestion.selected"
            :disabled="getCurrentQuestion.selected"
            @change="SetAnswer"
          />
          <span>{{ option }}</span>
        </label>
      </div>

      <button @click="NextQuestion" :disabled="!getCurrentQuestion.selected">
        {{
          getCurrentQuestion.index == questions.length - 1
            ? "Finish"
            : getCurrentQuestion.selected == null
            ? "Select an option"
            : "Next question"
        }}
      </button>
    </section>

    <section v-else>
      <h2>You have finished the quiz!</h2>
      <p>Your score is {{ score }}/{{ questions.length }}</p>
    </section>
  </main>
</template>

<script>
import { ref, computed } from "vue";
import { getQuizByName } from "@/services/quizzes.api";

export default {
  name: "QuizView",
  components: {},
  mounted() {
    const quiz = getQuizByName(this.$route.params.id);
    this.title = quiz.title;
    this.questions = quiz.preguntas;
    this.num_questions = quiz.preguntas.length;
    this.max_score = quiz.max_score;
    this.quizCompleted = false;

    this.currentQuestion = computed(() => {
      let question = this.questions[this.currentQuestion];
      question.index = this.currentQuestion;
      return question;
    });
    this.score = computed(() => {
      let value = 0;
      this.questions.map((q) => {
        if (q.selected != null && q.answer == q.selected) {
          console.log("correct");
          value++;
        }
      });
      return value;
    });
  },
  data() {
    return {
      title: "",
      questions: [],
      num_questions: 0,
      max_score: 0,
      quizCompleted: ref(false),
      currentQuestion: ref(0),
    };
  },
  methods: {
    computed: {
      score() {
        let value = 0;
        this.questions.map((q) => {
          if (q.selected != null && q.answer == q.selected) {
            console.log("correct");
            value++;
          }
        });
        return value;
      },
      getCurrentQuestion() {
        let question = this.questions[this.currentQuestion];
        question.index = this.currentQuestion;
        return question;
      },
    },
    NextQuestion() {
      if (this.currentQuestion < this.questions.length - 1) {
        this.currentQuestion++;
      } else {
        this.quizCompleted = true;
      }
    },
    SetAnswer() {
      this.questions[this.currentQuestion].selected =
        this.getCurrentQuestion.selected;
    },
  },
};
const questions = ref([
  {
    question: "What is Vue?",
    answer: 0,
    options: ["A framework", "A library", "A type of hat"],
    selected: null,
  },
  {
    question: "What is Vuex used for?",
    answer: 2,
    options: ["Eating a delicious snack", "Viewing things", "State management"],
    selected: null,
  },
  {
    question: "What is Vue Router?",
    answer: 1,
    options: [
      "An ice cream maker",
      "A routing library for Vue",
      "Burger sauce",
    ],
    selected: null,
  },
]);
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: "Montserrat", sans-serif;
}

body {
  background-color: #271c36;
  color: #fff;
}

.app {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
  height: 100vh;
}

h1 {
  font-size: 2rem;
  margin-bottom: 2rem;
}

.quiz {
  background-color: #382a4b;
  padding: 1rem;
  width: 100%;
  max-width: 640px;
}

.quiz-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.quiz-info .question {
  color: #8f8f8f;
  font-size: 1.25rem;
}

.quiz-info.score {
  color: #fff;
  font-size: 1.25rem;
}

.options {
  margin-bottom: 1rem;
}

.option {
  padding: 1rem;
  display: block;
  background-color: #271c36;
  margin-bottom: 0.5rem;
  border-radius: 0.5rem;
  cursor: pointer;
}

.option:hover {
  background-color: #2d213f;
}

.option.correct {
  background-color: #2cce7d;
}

.option.wrong {
  background-color: #ff5a5f;
}

.option:last-of-type {
  margin-bottom: 0;
}

.option.disabled {
  opacity: 0.5;
}

.option input {
  display: none;
}

button {
  appearance: none;
  outline: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem 1rem;
  background-color: #2cce7d;
  color: #2d213f;
  font-weight: 700;
  text-transform: uppercase;
  font-size: 1.2rem;
  border-radius: 0.5rem;
}

button:disabled {
  opacity: 0.5;
}

h2 {
  font-size: 2rem;
  margin-bottom: 2rem;
  text-align: center;
}

p {
  color: #8f8f8f;
  font-size: 1.5rem;
  text-align: center;
}
</style>
