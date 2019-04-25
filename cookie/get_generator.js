const s_tag = '<script>', e_tag = '</script>';
const cookie_tag = 'document.cookie=';

// Function to generate cookie
const generate_cookie = page =>  {
    // Get primary script
    const s_ind = page.indexOf(s_tag);
    const e_ind = page.indexOf(e_tag);

    // Remove additional actions
    let code = page.substring(s_ind + s_tag.length, e_ind);
    const e_brack = code.lastIndexOf('}') + 1;

    code = code.substring(0, e_brack);
    code += 'r;';

    // Generate secondary/cookie generator
    let secondary = eval(code);

    // Remove additional actions
    const rl_ind = secondary.lastIndexOf("'") + 2;
    secondary = secondary.substring(0, rl_ind);
    secondary = secondary.replace(cookie_tag, '');

    // Generate cookie
    let cookie = eval(secondary);
    const cookie_end = cookie.indexOf(';');
    cookie = cookie.substring(0, cookie_end);

    return cookie;
}

module.exports = {
    generate_cookie
};
