export function highlightText(text, searchTerm) {
  if (!searchTerm || !text) return text;
  
  const regex = new RegExp(`(${searchTerm})`, 'gi');
  const parts = text.split(regex);
  
  return parts.map((part, index) => 
    regex.test(part) 
      ? `<mark class="highlight">${part}</mark>`
      : part
  ).join('');
}

export function searchPrompts(prompts, searchTerm) {
  if (!searchTerm) return prompts;
  
  const term = searchTerm.toLowerCase();
  
  return prompts.filter(prompt => {
    const titleMatch = prompt.title?.toLowerCase().includes(term);
    const contentMatch = prompt.content?.toLowerCase().includes(term);
    const descMatch = prompt.description?.toLowerCase().includes(term);
    const tagsMatch = prompt.tags?.some(tag => tag.toLowerCase().includes(term));
    
    return titleMatch || contentMatch || descMatch || tagsMatch;
  });
}
