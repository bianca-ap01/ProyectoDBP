<template>
  <div>
    <div>
      <ul v-for="quiz in quizzes" :key="quiz.id">
        {{
          quiz.title
        }}
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: "ListarQuizzes",
  props: {
    quizzes: {
      type: [],
      required: true,
    },
  },
};
</script>
