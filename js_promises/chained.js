var step1 = new Promise ((resolve, reject) => {
  setTimeout(() => resolve("success in step1"), 1000)
})
var step2 = step1.then(
  msg => {
    console.log(msg);
    return new Promise((resolve, reject) => {
      setTimeout(() => reject(msg + ", error in step 2"), 1000)
    })
  }, 
  msg => console.log(msg)
);
var step3 = step2.then(
  msg => console.log("step 2 success - " + msg), 
  msg => console.log("step 2 error - " + msg), 
);

var interval = setInterval(() => {
  console.log('step1: ', step1);
  console.log('step2: ', step2);
  console.log('step3: ', step3);
}, 400);

setTimeout (function () {
  clearInterval(interval);
  console.log ('Asynchronous code completed');
}, 3000);

console.log ('step1: ', step1);
console.log ('step2: ', step2);
console.log('step3: ', step3);
console.log ('Synchronous code completed')
