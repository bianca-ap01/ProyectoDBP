<template>
  <div>
    <div v-for="quiz in allQuizzes" :key="quiz.id">
      <div>
        <router-link to="/quizzes/{{ quiz.id }}">{{ quiz.name }}</router-link>
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import { fetchSurveys } from "@/services/quizzes.api";

export default {
  name: "HomeView",
  components: {},
  mounted() {
    this.loadQuizzes();
  },
  data() {
    return {
      allQuizzes: [],
    };
  },
  methods: {
    async loadQuizzes() {
      const { success, quizzes, message } = await fetchSurveys();
      if (success) {
        console.log(quizzes);
        this.allQuizzes = quizzes;
        console.log(this.allQuizzes);
      } else {
        console.log(message);
      }
    },
  },
};
</script>
