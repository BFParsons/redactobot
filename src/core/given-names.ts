/**
 * @license
 * Copyright 2026 The Redactobot Authors
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Common given names and nicknames, used to recognise a first
 * name standing on its own ("Mateo will stay with Barbara") when no full name
 * gives it away. The list is deliberately broad rather than complete. It is
 * bundled with the app; nothing is looked up online.
 *
 * AMBIGUOUS holds names that are also ordinary English words or places. Those
 * are only treated as names when the sentence around them makes that clear.
 */

const split = (s: string) => new Set(s.trim().split(/\s+/));

/** Common given names and nicknames, in lower case. */
export const GIVEN_NAMES = split(`
aaliyah aaron abby abdul abdullah abel abigail abraham ada adam adebayo adela adele adeline adnan adrian adriana adrienne agnes ahmad ahmed aida aidan aiden aiko aisha akira al alan alana albert alberto aldo alejandra alejandro alex alexa alexander alexandra alexis alfonso alfred alfredo ali alice alicia alina alisha alison allan allen allison alma alonzo alvin alyssa amanda amara amari amelia amina amir amit amos amy ana anand anastasia andre andrea andres andrew andy angela angelica angelina angelo angie anika anil anita ann anna annabelle anne annette annie anthony antoine anton antonia antonio anya archie ari ariana ariel arjun arlene armando arnold arthur arturo asha ashley ashok aubrey audrey aurora ava avery ayesha
bailey barb barbara barney barry bart bartholomew bea beatrice beatriz becky belinda ben benedict benita benjamin bennett benny bernadette bernard bernice bernie bert bertha beth bethany betsy betty beverly bianca bjorn blake blanca bo bob bobbi bobby bonnie boris brad bradley brady brandi brandon brandy brenda brendan brent brett brian briana brianna bridget brigid britney brittany bruce bruno bryan bryce byron
caitlin caleb callum calvin cameron camila camille candace candice cara carl carla carlos carlton carmen carol carole caroline carolyn carrie carter casey cassandra cassie catalina catherine cathy cecil cecilia cedric celeste celia cesar chandra chantal charlene charles charlie charlotte chelsea cheryl chiara chidi chinedu chloe chris christa christina christine christopher chuck cindy claire clara clarence clarissa clark claude claudia clay clayton clement cleo clifford clint clinton clyde cody colin colleen connie connor conrad constance cora corey corinne cornelius cory courtney craig cristina crystal curtis cynthia cyrus
daisuke dalia damian damien damon dan dana daniel daniela danielle danny dante daphne darius darlene darnell darrell darren darryl dave david davina deanna deb debbie deborah debra declan deepak deirdre delia delores demetrius denise dennis derek derrick desiree desmond devin devon dewayne dexter diana diane dianne diego dimitri dina dinah dion dolores dominic dominique don donald donna donovan dora doreen doris dorothy doug douglas duane dustin dwayne dwight dylan
eamon ed eddie edgar edith edmund edna eduardo edward edwin eileen elaine eleanor elena eli elias elijah elisa elise elizabeth ella ellen ellie elliot elliott elmer eloise elsa elsie elvira emanuel emeka emil emilia emilio emily emma emmanuel emmett enrique eric erica erik erika erin ernest ernesto esperanza esteban estelle esther ethan ethel eugene eunice eva evan evelyn everett ezekiel ezra
fabian fabiola faisal farah fatima felicia felipe felix fernando fidel fiona flora floyd folasade frances francesca francine francis francisco frankie franklin fred freda freddie frederick frieda
gabe gabriel gabriela gabrielle gail garrett garry gary gavin gayle genevieve geoff geoffrey george georgina gerald geraldine gerard gerardo gertrude gil gilbert gina ginny giovanni gladys glenda glenn gloria gordon grady graham greg gregg gregory greta gretchen guadalupe guillermo gus gustavo gwen gwendolyn
hakeem hal hamid hana hank hannah hans harold harriet harrison harry harvey hassan hattie heather hector heidi helen helena helga henrietta henry herbert herman hilda hillary hiroshi howard hubert hugh hugo humberto hye-jin
ian ibrahim ida ignacio ike ikechukwu ilana imani imelda imran ines ingrid irene irma irving isaac isabel isabella isabelle isaiah ismael ivan ivana ivonne
jabari jackie jacob jacqueline jacques jada jaime jake jamal james jamie jan jana jane janelle janet janice janine jared jasmine jason javier jay jayden jean jeanette jeanne jeannie jeff jeffrey jen jenna jennie jennifer jenny jeremiah jeremy jerome jerry jesse jessica jessie jesus jill jillian jim jimmy jin jo joan joann joanna joanne joaquin jocelyn jodi jody joe joel joey johan johanna john johnny jon jonah jonas jonathan joni jorge jose josefina joseph josephine josh joshua josiah josie juan juana juanita judith judy jules julia julian juliana julie juliet julio julius jun justin justine
kai kaitlyn kamal kara kareem karen kari karim karina karl karla kate katelyn katherine kathleen kathryn kathy katie katrina katya kay kayla keisha keith kelly kelsey ken kendra kenji kenneth kenny kent kenya kerry kevin khalid kiara kieran kim kimberly kira kirk kirsten kofi krista kristen kristin kristina kristine kristy kurt kwame kyle kylie
lakshmi lamar lana larry latisha latoya laura laurel lauren laurence laurie lawrence layla lea leah leanne lee leigh leila lena leo leon leona leonard leonardo leroy leslie lester leticia levi lewis liam lila lillian lina linda lindsay lindsey ling lionel lisa liz liza lloyd logan lois lola lonnie lorena lorenzo loretta lori lorna lorraine lou louis louisa louise lourdes lucas lucia luciana lucille lucinda lucy luis luisa luke luther lydia lyle lynda lynette lynn
mabel mackenzie madeline mae maggie mahmoud maia malcolm malik mandy manny manuel marc marcel marcela marcella marcia marco marcos marcus margaret margarita margie margo marguerite mari maria mariam marian mariana marianne maribel marie marilyn marina mario marion marisa marisol marissa marjorie marla marlene marlon marsha marshall marta martha martin martina marty marvin mary maryam mason mateo matt matthew maude maura maureen maurice mavis max maxine maxwell maya meg megan meghan mehmet mei melanie melinda melissa melvin mercedes meredith mia michael michaela micheal michele michelle miguel mike mikhail mildred milo milton mimi mina mindy minh miranda miriam mitch mitchell mohamed mohammad mohammed moira molly mona monica monique morgan morris moses muhammad muriel murray mustafa myra myrna myron myrtle
nadia nadine nancy naomi natalia natalie natasha nate nathan nathaniel neal ned neha neil nell nellie nelson nia nicholas nick nicky nicola nicolas nicole nigel nikhil niki nikki nikolai nina nisha noah noel noelle nolan nora noreen norma norman nuno
octavia odessa ola olga oliver olivia ollie olu oluwaseun omar ophelia oren orlando oscar osvaldo otis otto owen
pablo paige pam pamela paolo patrice patricia patrick patsy patti patty paul paula paulette paulina pauline pedro peggy penelope percy perry pete peter petra phil philip phillip phoebe phyllis pierre piotr preston priscilla priya
quentin quincy quinn
rachel rafael raj rajesh ralph ramesh ramiro ramon ramona randall randy raphael raquel rashad rashid raul ravi raymond reba rebecca reggie regina reginald rene renee rex reza rhonda ricardo richard rick rickey ricky rigoberto riley rita robbie robert roberta roberto robin robyn rocco rochelle rod roderick rodney rodolfo rodrigo roger rohan roland rolando roman ron ronald ronnie roosevelt rory rosa rosalie rosalind rosario roscoe roseanne rosemary rosie roslyn ross roxanne roy royce ruben rudolph rudy rufus russ russell ruth ryan
sabrina sade sadie sal salma salvador sam samantha samir sammy samuel sana sandra sanjay santiago sara sarah sasha saul scott sean sebastian selena selma serena sergio seth seun shane shanice shannon shari sharon shaun shauna shawn shawna sheila shelby sheldon shelley shelly sheri sherman sherri sherry sheryl shirley sid sidney sierra silas silvia simon simone siobhan sofia sofía sonia sonja sonya sophia sophie spencer stacey stacy stan stanley stefan stella stephan stephanie stephen sterling steve steven stewart stu stuart sunil susan susanna susie suzanne sven svetlana sylvester sylvia
tabitha tamara tamika tammy tania tanisha tanya tara tariq tasha tatiana ted teddy terence teresa teri terrance terrell terrence terri terry tess tessa thaddeus thelma theo theodore theresa therese thomas tiffany tim timmy timothy tina tobias toby todd tom tomas tommy toni tonia tony tonya tracey traci tracy travis trent trevor trina trisha tristan troy trudy tucker ty tyler tyrone
ulysses uma ursula
val valentina valerie van vanessa vaughn vera vern verna vernon veronica vic vicki vickie vicky victor vijay vince vincent viola virgil vivian
wade wallace wally walt walter wanda warren wayne wendell wendy wes wesley whitney wilbert wilbur wilfred wilhelmina willa willard william willie willis wilma wilson winifred winnie winston wyatt
xavier ximena xiomara
yasmin yesenia yolanda yoshiko yuki yusuf yvette yvonne
zach zachary zane zara zeke zelda zoe zoey zora
`);

/**
 * Given names that are also ordinary English words or places, in lower case.
 */
export const AMBIGUOUS_NAMES = split(`
april may june august summer autumn dawn eve
grace faith hope joy charity mercy patience destiny serenity trinity harmony
hunter chase mark bill will rob pat sue drew art gene guy jack earl dean grant ward miles rich lance cliff dale glen heath lane brook clay reed rex roy ray rod don dot bud buddy sonny skip chip norm frank
jordan paris georgia virginia carolina dakota austin dallas savannah madison lincoln jackson sydney victoria florence israel chad kenya india asia china
rose ruby pearl opal amber jade ivy holly iris lily daisy violet hazel olive penny sandy rusty rocky angel christian
`);
