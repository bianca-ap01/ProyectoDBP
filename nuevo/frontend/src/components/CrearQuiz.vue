<template>
  <div>
    <h1 class="title">Crear Quiz</h1>
    <div v-if="!isUserSubmitted">
      <form @submit.prevent.stop="signUpEvent" class="form">
        <div class="form-group">
          <label class="label">Titulo: </label>
          <input type="text" v-model="quiz.title" class="input" />
        </div>
        <div class="form-group">
          <label class="label">Número de preguntas:</label>
          <input type="number" v-model="quiz.num_preg" class="input" />
        </div>
        <div class="form-group">
          <label class="label">Puntaje máximo:</label>
          <input type="password" v-model="quiz.max_score" class="input" />
        </div>
        <button class="submit-button" type="submit">Crear</button>
      </form>
    </div>
  </div>
</template>
<script>
import { createQuiz } from "@/services/quizzes.api";

export default {
  name: "CrearQuiz",
  data() {
    return {
      quiz: {
        title: "",
        num_preg: 0,
        max_score: 0,
      },
    };
  },
  methods: {
    createQuizLocal() {
      createQuiz();
    },
  },
};
</script>

<style></style>
