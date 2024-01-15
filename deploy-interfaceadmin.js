import chalk from 'chalk'
import { execa, $ } from 'execa'
import { root } from './src/git-utils.js'
import iValidate from './src/iValidate.js'
import inquirer from 'inquirer'

// const avec les chemins
const workspaceRoot = await root()
const dockerfilePath = `${workspaceRoot}/services/matchpy/app`
const dockerimagePath = 'europe-west1-docker.pkg.dev/dashemploi/dashemploi-images/interfaceadmin'


// Demander sur quel environnement on veut déployer
const environementChoices = await inquirer.prompt([
  {
    type: 'checkbox',
    name: 'environment',
    message: `Hello Pierre!
    Sur quel environnement veux-tu déployer ton interface aujourd'hui?`,
    choices: [
      { name: chalk.green('Développement (dev)'), value: 'dev' },
      { name: chalk.red('Production (prod)'), value: 'prod' },
    ],
    validate: function (answer) {
      if (answer.length < 1) {
        return 'Veuillez choisir au moins un environnement.'
      }
      return true
    },
  },
])

//
const selectedEnvironment = environementChoices.environment[0]
console.log(selectedEnvironment)

let deployEnvironnement = selectedEnvironment === 'dev' ? 'interfaceadmin-test' : 'interfaceadmin'
console.log(deployEnvironnement)

//Véifier si Docker est en marche
try {
  await execa('docker', ['stats', '--no-stream'])
} catch (e) {
  console.log(
    chalk.bgRed(
      'Docker is not running. Start it on your side then validate here'
    )
  )
  await iValidate('Docker is now started on the machine')
}
console.log('Start building the requirement container')

// build premiere image docker
// @todo faire un fichier config avec les chemins et tout parce que la c'est pas ouf en terme d'évolution du bouzin
//
// @togo faire une gestion =>
await execa('docker', [
  'build',
  '--rm',
  '-f',
  `${dockerfilePath}/requirements.dockerfile`,
  '-t',
  'requirements:latest',
  `${dockerfilePath}`,
])
console.log('Start building the  app container')
//build deuxième image docker

await execa('docker', [
  'build',
  '--rm',
  '-f',
  `${dockerfilePath}/app.dockerfile`,
  '-t',
  `interfaceadmin:${selectedEnvironment}`,
  `${dockerfilePath}`,
])

// push sur google artifact registry
console.log('Start tagging the image')

await execa('docker', [
  'tag',
  `interfaceadmin:${selectedEnvironment}`,
  `${dockerimagePath}:${selectedEnvironment}`,
])

console.log('Start pushing on Artifact Registry')
await execa('docker', [
  'push',
  `${dockerimagePath}:${selectedEnvironment}`,
])

console.log('Succefully Pushed')

// push sur google cloud run
console.log('Deploying on cloud run ')

await execa(
  'gcloud',
  [
    'run',
    'deploy',
    `${deployEnvironnement}`,
    `--image=${dockerimagePath}:${selectedEnvironment}`,
    '--region=europe-west1',
    '--memory=1G',
    '--allow-unauthenticated',
  ],
  { stdio: 'inherit' }
)
